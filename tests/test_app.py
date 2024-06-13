from flask import session, g, url_for
import openai
import openai_responses
from openai_responses import OpenAIMock
from unittest.mock import patch
from ramenai.main import app
import ramenai.views

# import ramenai.db
import secrets


def test_login_despliega(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Log In con Google" in response.data


def test_login_redirige_google(client):
    response = client.post("/login")
    assert response.status_code == 302
    assert "location" in response.headers
    redirect_url = response.headers["location"]
    assert redirect_url.startswith("https://accounts.google.com/o/oauth2/v2/auth")


@patch("ramenai.auth.google.authorize_access_token")
def test_authorized(mock_authorize_access_token, client):
    mock_authorize_access_token.return_value = {"userinfo": {"name": "Test User"}}
    with app.app_context():
        response = client.get("/auth/login/authorized", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["Location"] == "/"

    with client.session_transaction() as sess:
        assert sess["user"] == "Test User"


def test_logout(client):
    with client.session_transaction() as sess:
        sess["user"] = "Test User"
    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert "Has cerrado sesión exitosamente" in response.data.decode("utf-8")

    with client.session_transaction() as sess:
        assert "user" not in sess
    assert response.request.path == "/login"


def test_chat_display_ok(client):
    with client.session_transaction() as sess:
        sess["user"] = "Test User"
    response = client.get("/")
    assert response.status_code == 200
    assert "maruchat" in response.data.decode("utf-8")


def test_chat_display_error(client):
    response = client.get("/", follow_redirects=True)
    assert len(response.history) == 1
    assert response.history[0].status == "302 FOUND"
    assert response.request.path == "/login"
    assert "Por favor ingresa a sesión" in response.data.decode("utf-8")


""" @openai_responses.mock()
def test_create_chat_completion(openai_mock: OpenAIMock):
    openai_mock.chat.completions.create.response = {
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {"content": "¡Hola! ¿En qué puedo ayudarte hoy?", "role": "assistant"},
            }
        ]
    }

    client = openai.Client(api_key="sk-fake123")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un excelente cocinero y experto en ramen. Eres bueno en descubrir e inventar nuevas formas de preparar y disfrutar ramen en casa. Das recetas sencillas e instrucciones concisas."},
            {"role": "user", "content": "Dame una receta de ramen de pollo"},
        ],
    )

    assert len(completion.choices) == 1
    assert completion.choices[0].message.content == "Hello! How can I help?"
    assert openai_mock.chat.completions.create.route.call_count == 1 """