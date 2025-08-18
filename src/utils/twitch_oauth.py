from json import load as json_load
from os import path


def get_twitch_tokens(CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str) -> dict | None:
    if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
        print("Missing required environment variables.")
        return None
    
    tokens_path = path.join("src", "data", "tokens.json")

    if not path.exists(tokens_path):
        print("Tokens file does not exist. Please run the OAuth flow first.")
        return None

    with open(tokens_path, "r") as f:
        tokens = json_load(f)

    return tokens

