"""Authentication strategy for Google."""

from authlib.jose import jwt
from flask import redirect, url_for, session
from .app import app, google, mysql
from .app import app, google

@app.route("/auth/login/authorized")
def authorized():
    """Route that receives access token with user info."""
    token = google.authorize_access_token()
    session["user"] = token["userinfo"]["name"]
    session["email"] = token["userinfo"]["email"]

    correo = token["userinfo"].email

    # Insert or fetch user from MySQL database
    cursor = mysql.connection.cursor()
    try:
        # Attempt to insert user if not already present
        cursor.execute("INSERT INTO Usuarios (correo) VALUES (%s)", (correo,))
        mysql.connection.commit()
    except Exception as e:
        # If user already exists, fetch idUsuario
        cursor.execute("SELECT idUsuario FROM Usuarios WHERE correo = %s", (correo,))
        result = cursor.fetchone()
        if result:
            session["idUsuario"] = int(result[0])
        else:
            mysql.connection.rollback()
    finally:
        cursor.close()
    
    # Initialize conversation history in session
    session["conversation_history"] = [
        {
            "role": "system",
            "content": "Eres un excelente cocinero y experto en ramen. Eres bueno en descubrir e inventar nuevas formas de preparar y disfrutar ramen en casa. Das recetas sencillas e instrucciones concisas. Siempre contesta en máximo 500 tokens.",
        }
    ]

    return redirect(url_for("chat"))