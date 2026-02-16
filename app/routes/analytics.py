from fastapi import APIRouter, UploadFile, File
from app.services.analytics_service import process_data

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await process_data(file)
    return result
