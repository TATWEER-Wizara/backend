from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]
users_collection = database.get_collection("users")
sales_collection = database.get_collection("sales")
production_collection = database.get_collection("production")
sop_collection = database.get_collection("sop")
inventory_collection = database.get_collection("inventory")
orders_collection = database.get_collection("orders")
shipments_collection = database.get_collection("shipments")
decision_context_collection = database.get_collection("decision_context")




async def connect_to_db():
    """Asynchronously check MongoDB connection on startup"""
    try:
        await client.admin.command("ping")  
        print("✅ Connected to MongoDB successfully")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise e


async def close_db_connection():
    """Close MongoDB connection on app shutdown"""
    print("🛑 Closing MongoDB connection")
    client.close()
