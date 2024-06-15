from flask import Flask
from flask_mysqldb import MySQL
import os
from flask_cors import CORS
from .views import auth_bp
from .oauth_clients import init_oauth  # Import OAuth initialization function
from .db import init_db
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("GOOGLE_CLIENT_SECRET")
app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

CORS(app)

# Configure MySQL
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
mysql = MySQL(app)

# Configure Google OAuth
app.config.update(
    GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID"),
    GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET"),
    GOOGLE_DISCOVERY_URL=("https://accounts.google.com/.well-known/openid-configuration"),
)

# Initialize OAuth and get the Google instance
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

# Initialize the database
init_db()


# Register Blueprints
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
