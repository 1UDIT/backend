from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.db import users_collection

router = APIRouter()

class UserCreate(BaseModel):
    userName: str
    password: str
    role: str

@router.post("/")
async def create_user(user: UserCreate):

    await users_collection.insert_one(user.model_dump())

    return {"message": "User created successfully"}