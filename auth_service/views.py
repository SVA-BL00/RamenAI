from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .db import get_db
import requests


auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in route handling both GET and POST requests."""
    from .app import google  # Import OAuth clients dictionary

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        redirect_uri = url_for("auth.authorized", _external=True)
        return google.authorize_redirect(redirect_uri)

@auth_bp.route("/logout")
def logout():
    """Log out."""
    session.clear()
    flash("Has cerrado sesión exitosamente")
    return redirect(url_for("auth.login"))

@auth_bp.route("/login/authorized")
def authorized():
    """Route that receives access token with user info."""

    from .app import google 

    token = google.authorize_access_token()
    session["user"] = token["userinfo"]["name"]
    session["email"] = token["userinfo"]["email"]

    correo = token["userinfo"]["email"]

    from .app import mysql

    # Insert or fetch user from MySQL database
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO Usuarios (correo) VALUES (%s)", (correo,))
        get_db().commit()
    except Exception as e:
        cursor.execute("SELECT idUsuario FROM Usuarios WHERE correo = %s", (correo,))
        result = cursor.fetchone()
        if result:
            session["idUsuario"] = int(result[0])
        else:
            get_db().rollback()
    finally:
        cursor.close()

    session["conversation_history"] = [
        {
            "role": "system",
            "content": "Eres un excelente cocinero y experto en ramen. Eres bueno en descubrir e inventar nuevas formas de preparar y disfrutar ramen en casa. Das recetas sencillas e instrucciones concisas. Siempre contesta en máximo 500 tokens.",
        }
    ]

    if "user" not in session:
        flash("Por favor ingresa a sesión")
        return redirect(url_for("auth.login"))
    
    
    # Inter-service communication to chat_service
    chat_service_url = "http://chat_service:5001/chat"
    response = requests.get(chat_service_url)
    print("RESPONSE")
    print(response)
    if response.status_code == 200:
        return redirect(url_for('chat.chat'))
    else:
        flash("Error connecting to chat service")
        return redirect(url_for('auth.login'))
