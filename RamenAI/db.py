"""Database handling."""

import os
from pymongo import MongoClient
from .app import app


def get_db():
    """Getter for database."""
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["maruchat"]


def init_db():
    """Initialize database."""
    db = get_db()
    conversations_collection = db["conversations"]
    return conversations_collection
