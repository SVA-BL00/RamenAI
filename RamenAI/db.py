import os
from pymongo import MongoClient
from .app import app



def get_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["maruchat"]


def init_db():
    db = get_db()
    conversations_collection = db["conversations"]
    return conversations_collection
