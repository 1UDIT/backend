import pandas as pd
from io import BytesIO

async def process_data(file):
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))

    df["Revenue"] = df["Quantity"] * df["Price"]
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    total_revenue = float(df["Revenue"].sum())
    total_orders = int(df["OrderID"].nunique())
    avg_order_value = float(df["Revenue"].mean())

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

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "monthly_sales": monthly_sales,
        "top_products": top_products
    }
