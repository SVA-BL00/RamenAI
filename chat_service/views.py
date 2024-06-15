import datetime
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
import openai
from .db import get_db
import os

chat_bp = Blueprint('chat', __name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@chat_bp.route("/chat")
def chat():
    """Index route that includes chat."""
    if "user" not in session:
        flash("Por favor ingresa a sesión")
        return redirect(url_for("auth.login"))

    try:
        db = get_db()
        conversations_collection = db['conversations']
        user_id = session.get('idUsuario')

        conversation_history = list(conversations_collection.find({"userId": user_id}))

        conversation_history = [message for message in conversation_history if message["role"] != "system"]

        return render_template("chat.html", conversation_history=conversation_history)

    except Exception as e:
        print(f"Error fetching conversation history: {e}")
        flash("Error fetching conversation history")
        return redirect(url_for("auth.login"))

@chat_bp.route("/api/maruchat", methods=["POST"])
def maruchat():
    """API post to get maruchat."""
    try:
        db = get_db()
        conversations_collection = db["conversations"]

        user_id = session.get('idUsuario')

        if user_id is None:
            return jsonify({"error": "User ID is null, cannot save conversation in MonoDB."}), 400

        conversation_history = session.get("conversation_history", [])
        user_input = request.json.get('userInput')

        if user_input:
            conversation_history.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            max_tokens=500,
            stop=None,
        )

        chat_response = response.choices[0].message["content"]
        conversation_history.append({"role": "assistant", "content": chat_response})

        conversation_records = [
            {
                "userId": user_id,
                "role": message["role"],
                "content": message["content"],
                "timestamp": datetime.datetime.now(),
            }
            for message in conversation_history
        ]

        conversations_collection.insert_many(conversation_records)

        return jsonify({"chatResponse": chat_response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
