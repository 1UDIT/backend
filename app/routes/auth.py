from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel
from app.utils.db import users_collection, analytics_collection 
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter() 




class LoginRequest(BaseModel):
    userName: str
    password: str

@router.post("/")
@limiter.limit("5/minute")
async def login(request: Request, data: LoginRequest): 

    user = await users_collection.find_one(
        {"userName": data.userName}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "userName": user["userName"],
        "role": user["role"],
    }

# @router.get("/admin/data")
# async def admin_data(role: str):

#     if role != "admin":
#         raise HTTPException(
#             status_code=403,
#             detail="Access denied"
#         )

#     data = await analytics_collection.find().to_list(100)

#     for doc in data:
#         doc["_id"] = str(doc["_id"])

#     return data
 

@router.get("/files")
async def get_files(username: str = Query(...), role: str = Query(...)):

    # Admin can see all files
    if role == "admin":
        files = await analytics_collection.find(
            {},
            {"filename": 1, "uploaded_at": 1, "username": 1, "role":1}
        ).to_list(100)

    # Normal user sees only their files
    else:
        files = await analytics_collection.find(
            {"username": username},
            {"filename": 1, "uploaded_at": 1, "role":1, "username": username}
        ).to_list(100)

    for f in files:
        f["_id"] = str(f["_id"])

    return files