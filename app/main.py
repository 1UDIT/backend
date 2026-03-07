from fastapi import FastAPI
from app.routes.analytics import router as analytics_router
from app.routes.createUser import router as createUser
from app.utils.db import client


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(analytics_router, prefix="/analytics")
app.include_router(createUser, prefix="/createUser")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Business Analytics API Running 🚀"}

@app.on_event("startup")
async def startup_db_check():
    try:
        await client.admin.command("ping")
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise e
