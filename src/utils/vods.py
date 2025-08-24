import requests


def get_all_vods(CLIENT_ID: str, ACCESS_TOKEN: str, USER_ID: str):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    params = {
        "user_id": USER_ID
    }

    response = requests.get("https://api.twitch.tv/helix/videos", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve VODs:", response.status_code, response.text)
        return None


def get_latest_vod(CLIENT_ID: str, ACCESS_TOKEN: str, USER_ID: str):
    all_vods = get_all_vods(CLIENT_ID, ACCESS_TOKEN, USER_ID)


if __name__ == "__main__":
    from dotenv import load_dotenv
    from os import getenv
    from twitch_oauth import get_saved_twitch_tokens
    from user_data import get_user_data

    load_dotenv()

    CLIENT_ID = getenv("TWITCH_CLIENT_ID")
    ACCESS_TOKEN = get_saved_twitch_tokens()["access_token"]
    USER_ID = get_user_data(CLIENT_ID, ACCESS_TOKEN)["id"]

    print("VOD data:", CLIENT_ID, ACCESS_TOKEN, USER_ID, sep="\n")

    vod_data = get_all_vods(CLIENT_ID, ACCESS_TOKEN, USER_ID)
    print("VOD data:", vod_data)
