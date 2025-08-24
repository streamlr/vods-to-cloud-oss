import requests


def get_user_data(CLIENT_ID: str, ACCESS_TOKEN: str):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get("https://api.twitch.tv/helix/users", headers=headers)

    if response.status_code == 200:
        return response.json()['data'][0]
    else:
        print("Failed to retrieve user data:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    import os
    from twitch_oauth import get_saved_twitch_tokens
    from dotenv import load_dotenv

    load_dotenv()

    CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    ACCESS_TOKEN = get_saved_twitch_tokens()["access_token"]

    user_data = get_user_data(CLIENT_ID, ACCESS_TOKEN)
    if user_data:
        print(user_data)
