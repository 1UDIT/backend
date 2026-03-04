from fastapi import APIRouter, UploadFile, File, Form
from app.services.analytics_service import process_data
from app.utils.db import analytics_collection

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    username: str = Form(...)
):
    result = await process_data(file, username)
    return result

@router.get("/data")
async def get_latest_analytics():
    latest = await analytics_collection.find_one({}, sort=[("_id", -1)])

    if not latest:
        return {"message": "No data available"}

    latest["_id"] = str(latest["_id"])  # Convert ObjectId → string
    return latest