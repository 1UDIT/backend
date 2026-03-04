import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pymongo.errors import PyMongoError

# Load environment variables
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

# 🔴 1️⃣ Validate ENV variables 

if not MONGO_URL:
    print("❌ MONGO_URL is not set in .env file")
    sys.exit(1)

if not DB_NAME:
    print("❌ DB_NAME is not set in .env file")
    sys.exit(1)

try:
    # 🔵 2️⃣ Create client
    client = AsyncIOMotorClient(
        MONGO_URL,
        serverSelectionTimeoutMS=5000  # 5 seconds timeout
    )

    db = client[DB_NAME]
    analytics_collection = db["analytics"]

    print("✅ MongoDB connection initialized")

except PyMongoError as e:
    print(f"❌ MongoDB connection error: {e}")
    sys.exit(1)