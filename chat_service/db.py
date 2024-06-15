from pymongo import MongoClient
import os

def get_db():
    """Getter for database."""
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["chat_service_db"]

def init_db():
    """Initialize database."""
    db = get_db()
    conversations_collection = db["conversations"]
    return conversations_collection
