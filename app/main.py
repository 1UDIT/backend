from fastapi import FastAPI
from app.routes.analytics import router as analytics_router
from app.routes.createUser import router as createUser
from app.routes.auth import router as login,  limiter
from app.utils.db import client

from fastapi.middleware.cors import CORSMiddleware

# SlowAPI imports
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


app = FastAPI()

# attach limiter
app.state.limiter = limiter

# register error handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# add middleware
app.add_middleware(SlowAPIMiddleware)


app.include_router(analytics_router, prefix="/analytics")
app.include_router(createUser, prefix="/createUser")
app.include_router(login, prefix="/login")

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