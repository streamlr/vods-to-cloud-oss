from dotenv import load_dotenv
from flask import Flask, request, redirect
from json import dump as json_dump
from dotenv import load_dotenv
from src.utils import get_auth_url, get_twitch_tokens_from_server
import os
import requests
import urllib.parse

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

app = Flask(__name__)

f_tokens: str | None = None


@app.route("/")
def index():
    auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)
    return f'<a href="{auth_url}">Login with Twitch</a>'


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: no se recibió el code", 400

    tokens = get_twitch_tokens_from_server(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, code)

    with open("src/data/tokens.json", "w") as f:
        json_dump(tokens, f)

    return f"Logging successful"


app.run(port=5000, debug=True)
