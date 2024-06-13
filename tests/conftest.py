# conftest.py
import mongomock
import pytest_mock as mocker
import pytest
from ramenai.app import app as appli
from ramenai.db import get_db, init_db


@pytest.fixture(scope="session")
def mock_database_client():
    return mongomock.MongoClient()


@pytest.fixture
def app(mocker, mock_database_client):
    def mock_get_db():
        return mock_database_client["maruchat"]

    def mock_init_db():
        db = mock_get_db()
        conversations_collection = db["conversations"]
        return conversations_collection

    # Patch 'ramenai.db.get_db' and 'ramenai.db.init_db'
    mocker.patch("ramenai.db.get_db", mock_get_db)
    mocker.patch("ramenai.db.init_db", mock_init_db)

    appli.config["SERVER_NAME"] = "127.0.0.1:5000"
    appli.config["APPLICATION_ROOT"] = "/"
    appli.config["PREFERRED_URL_SCHEME"] = "http"
    appli.testing = True
    yield appli


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
