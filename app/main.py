from fastapi import FastAPI
from app.routes.analytics import router as analytics_router

app = FastAPI()

app.include_router(analytics_router, prefix="/analytics")

@app.get("/")
def root():
    return {"message": "Business Analytics API Running 🚀"}
