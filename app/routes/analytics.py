from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.analytics_service import process_data
from app.utils.db import analytics_collection
from bson import ObjectId
router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    username: str = Form(...),
    role: str = Form(...)
):
    result = await process_data(file, username, role)
    return result



@router.get("/data/{dataset_id}")
async def get_data(dataset_id: str):

    data = await analytics_collection.find_one({
        "_id": ObjectId(dataset_id)
    })

    if not data:
        raise HTTPException(status_code=404, detail="Dataset not found")

    data["_id"] = str(data["_id"])

    return data

@router.delete("/delete/{dataset_id}")
async def delete_dataset(dataset_id: str, username: str, role: str): 
    if role == "admin":
        result = await analytics_collection.delete_one({
            "_id": ObjectId(dataset_id)
        })

    else:
        result = await analytics_collection.delete_one({
            "_id": ObjectId(dataset_id),
            "username": username
        })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return {"message": "Dataset deleted successfully"}