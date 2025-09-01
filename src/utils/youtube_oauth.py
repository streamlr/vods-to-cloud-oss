import json
import time
from os import path
import urllib.parse
import requests


# Where YouTube tokens will be persisted
yt_tokens_path = path.join("src", "data", "yt_tokens.json")


def yt_get_auth_url(CLIENT_ID: str, REDIRECT_URI: str) -> str:
    """Builds the Google OAuth URL for YouTube uploads scope.

    Scopes: https://www.googleapis.com/auth/youtube.upload
    We request offline access so we can refresh tokens.
    """
    scope = [
        "https://www.googleapis.com/auth/youtube.upload",
    ]
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scope),
        "access_type": "offline",
        "include_granted_scopes": "true",
        # force consent to ensure refresh_token on first run
        "prompt": "consent",
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"


def yt_exchange_code_for_tokens(CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str, code: str) -> dict:
    """Exchanges an authorization code for access and refresh tokens and saves them."""
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    resp = requests.post(token_url, data=data)
    resp.raise_for_status()
    tokens = resp.json()

    # enrich with an absolute expiry timestamp for convenience
    if "expires_in" in tokens:
        tokens["expires_at"] = int(time.time()) + int(tokens["expires_in"]) - 30  # small buffer

    with open(yt_tokens_path, "w") as f:
        json.dump(tokens, f)

    return tokens


def yt_get_saved_tokens() -> dict | None:
    if not path.exists(yt_tokens_path):
        return None
    with open(yt_tokens_path, "r") as f:
        tokens = json.load(f)
    return tokens


def yt_save_tokens(tokens: dict) -> None:
    with open(yt_tokens_path, "w") as f:
        json.dump(tokens, f)


def yt_refresh_access_token(CLIENT_ID: str, CLIENT_SECRET: str) -> dict | None:
    tokens = yt_get_saved_tokens()
    if not tokens or "refresh_token" not in tokens:
        return None

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
    }
    resp = requests.post(token_url, data=data)
    resp.raise_for_status()
    new_tokens = resp.json()

    # keep existing refresh_token if not returned
    if "refresh_token" not in new_tokens:
        new_tokens["refresh_token"] = tokens.get("refresh_token")

    if "expires_in" in new_tokens:
        new_tokens["expires_at"] = int(time.time()) + int(new_tokens["expires_in"]) - 30

    yt_save_tokens(new_tokens)
    return new_tokens


def yt_get_valid_access_token(CLIENT_ID: str, CLIENT_SECRET: str) -> str | None:
    """Returns a valid access token, refreshing if needed."""
    tokens = yt_get_saved_tokens()
    if not tokens:
        return None

    now = int(time.time())
    expires_at = tokens.get("expires_at")
    if not expires_at or now >= int(expires_at):
        refreshed = yt_refresh_access_token(CLIENT_ID, CLIENT_SECRET)
        if not refreshed:
            return None
        return refreshed.get("access_token")

    return tokens.get("access_token")
