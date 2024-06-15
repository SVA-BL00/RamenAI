import os
from pymongo import MongoClient
from flask_mysqldb import MySQL

def get_db():
    """Getter for MongoDB."""
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["auth_service_db"]

def init_db():
    """Initialize MongoDB."""
    db = get_db()
    users_collection = db["users"]
    return users_collection
