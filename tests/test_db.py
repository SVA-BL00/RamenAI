import os
import pytest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from ramenai.db import get_db, init_db


@pytest.fixture
def mock_mongo_client():
    with patch("pymongo.MongoClient") as mock:
        yield mock


def test_get_db(mock_mongo_client):
    mock_os = MagicMock()
    mock_os.getenv.return_value = "mongodb://localhost:27017/"

    with patch.dict(os.environ, {"MONGO_URI": "mongodb://localhost:27017/"}):

        db_client = get_db()

        assert db_client is not None
        assert isinstance(db_client, Database)


def test_init_db(mock_mongo_client):

    mock_db = MagicMock(spec=Database)
    mock_mongo_client.return_value.__getitem__.return_value = mock_db

    conversations_collection = init_db()

    # Assertions
    assert conversations_collection is not None
    assert isinstance(conversations_collection, Collection)
