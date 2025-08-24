from json import load as json_load
from os import path
import requests
import urllib


def get_auth_url(CLIENT_ID: str, REDIRECT_URI: str) -> str:
    scope = ["user:read:broadcast"]
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scope)
    } 
    auth_url = f"https://id.twitch.tv/oauth2/authorize?{urllib.parse.urlencode(params)}"
    return auth_url


def get_twitch_tokens_from_server(CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str, code: str) -> dict:
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
    return tokens


def get_saved_twitch_tokens() -> dict | None:
    tokens_path = path.join("src", "data", "tokens.json")

    if not path.exists(tokens_path):
        print("Tokens file does not exist. Please run the OAuth flow first.")
        return None

    with open(tokens_path, "r") as f:
        tokens = json_load(f)

    if "access_token" not in tokens:
        print("Access token is missing. Please run the OAuth flow first.")
        return None

    return tokens

