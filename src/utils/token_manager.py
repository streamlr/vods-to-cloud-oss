from json import dump
import requests
import os


def refresh_token(CLIENT_ID: str, CLIENT_SECRET: str, REFRESH_TOKEN: str):
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def get_access_token_from_refresh(CLIENT_ID: str, CLIENT_SECRET: str, REFRESH_TOKEN: str):
    refresh_token_data = refresh_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

    if refresh_token_data is None:
        raise Exception("Failed to refresh token")

    token_path = os.path.join("src", "data", "tokens.json")
    with open(token_path, "w") as token_file:
        dump(refresh_token_data, token_file)

    return refresh_token_data


if __name__ == "__main__":
    get_access_token_from_refresh("your_client_id", "your_client_secret", "your_refresh_token")
