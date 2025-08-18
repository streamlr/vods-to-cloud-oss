from dotenv import load_dotenv
from flask import Flask, request, redirect
from json import dump as json_dump
from dotenv import load_dotenv
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
    scope = ["user:read:broadcast"]
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scope)
    } 
    auth_url = f"https://id.twitch.tv/oauth2/authorize?{urllib.parse.urlencode(params)}"
    return f'<a href="{auth_url}">Login with Twitch</a>'


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: no se recibió el code", 400

    token_url = "https://id.twitch.tv/oauth2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    resp = requests.post(token_url, data=data)
    tokens = resp.json()

    with open("src/data/tokens.json", "w") as f:
        json_dump(tokens, f)

    return f"Logging successful"


app.run(port=5000, debug=True)
