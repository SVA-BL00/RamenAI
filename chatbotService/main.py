"""Main file to run the chatbot service"""

from app import app  # Adjust the import path based on your actual project structure
from views import *  # Adjust the import path based on your actual project structure

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
