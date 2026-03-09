import pandas as pd
from io import BytesIO
import numpy as np
from app.utils.db import analytics_collection
from datetime import datetime
from fastapi import HTTPException


async def process_data(file, username: str):

    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))

    df["Revenue"] = df["Quantity"] * df["Price"]
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    total_revenue = float(df["Revenue"].sum())
    total_orders = int(df["OrderID"].nunique())
    avg_order_value = float(df["Revenue"].mean())
    revenue_std = float(np.std(df["Revenue"]))

    monthly_sales = (
        df.groupby("Month")["Revenue"]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    top_products = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
        .to_dict(orient="records")
    )

    filename = file.filename

    result = {
        "username": username,
        "filename": filename,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "monthly_sales": monthly_sales,
        "top_products": top_products,
        "revenue_volatility": revenue_std,
        "uploaded_at": datetime.utcnow()
    }

    # Check if file already exists
    existing = await analytics_collection.find_one({
        "username": username,
        "filename": filename
    })

    # If file exists → update (doesn't count toward limit)
    if existing:
        await analytics_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": result}
        )
        result["_id"] = str(existing["_id"])
        return result

    # Count how many files user already has
    file_count = await analytics_collection.count_documents({
        "username": username
    })

    if file_count >= 3:
        raise HTTPException(
            status_code=400,
            detail="Upload limit reached. Maximum 3 files allowed."
        )

    # Insert new dataset
    inserted = await analytics_collection.insert_one(result)
    result["_id"] = str(inserted.inserted_id)

    return result