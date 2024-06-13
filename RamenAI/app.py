"""Defines app global configurations."""

import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_mysqldb import MySQL
from authlib.integrations.flask_client import OAuth
import secure


load_dotenv()


app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.urandom(24)


app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")


# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
mysql = MySQL(app)


secure_headers = secure.Secure(server=secure.Server())

CORS(app)


@app.after_request
def set_secure_headers(response):
    """Returns response object before going to client, used for testing."""
    secure_headers.framework.flask(response)
    return response


oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

