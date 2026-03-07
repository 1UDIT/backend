from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.db import users_collection
from fastapi import HTTPException
from app.utils.db import analytics_collection

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(data: LoginRequest):

    user = await users_collection.find_one(
        {"username": data.username}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "username": user["username"],
        "role": user["role"]
    }

@router.get("/admin/data")
async def admin_data(role: str):

    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    data = await analytics_collection.find().to_list(100)

    for doc in data:
        doc["_id"] = str(doc["_id"])

    return data