import requests


def get_user_data(CLIENT_ID: str, ACCESS_TOKEN: str):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get("https://api.twitch.tv/helix/users", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve user data:", response.status_code, response.text)
        return None
