from flask import session, redirect, url_for
from .app import google  # Import OAuth clients dictionary

def authorized():
    """Route that receives access token with user info."""
    
    token = google.authorize_access_token()
    session["user"] = token["userinfo"]["name"]
    session["email"] = token["userinfo"]["email"]

    correo = token["userinfo"].get("email")

    # Import get_db here to avoid circular import
    from db import get_db  

    # Insert or fetch user from MySQL database
    cursor = get_db().cursor()
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

    return redirect(url_for("chat"))
