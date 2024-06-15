from flask import Flask
import os
from .views import chat_bp
from .db import init_db, get_db

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

init_db()

from .views import *  # Import views at the end to avoid circular imports

# Register Blueprints
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
