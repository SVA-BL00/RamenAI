from authlib.jose import jwt
from flask import redirect, url_for, session
from .app import app, google, mysql
from .app import app, google

@app.route("/auth/login/authorized")
def authorized():
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
            print("sessionidUsuario")
            print(session["idUsuario"])
        else:
            mysql.connection.rollback()
    finally:
        cursor.close()

    return redirect(url_for("chat"))