from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "business_analytics")

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


def connect_to_mongo() -> AsyncIOMotorClient:
    global client, db

    if not MONGO_URL:
        raise RuntimeError("MONGO_URL is missing")
    if not DB_NAME:
        raise RuntimeError("DB_NAME is missing")

    client = AsyncIOMotorClient(
        MONGO_URL,
        maxPoolSize=50,
        minPoolSize=5,
        maxIdleTimeMS=30000,
        serverSelectionTimeoutMS=5000,
        socketTimeoutMS=20000,
        connectTimeoutMS=10000,
        server_api=ServerApi("1"),
    )

    db = client[DB_NAME]
    return client


def get_db() -> AsyncIOMotorDatabase:
    if db is None:
        raise RuntimeError("Database connection is not initialized")
    return db


def close_mongo_connection():
    global client
    if client:
        client.close()