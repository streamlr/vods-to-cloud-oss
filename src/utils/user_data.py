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


def get_user_id(CLIENT_ID: str, ACCESS_TOKEN: str):
    user_data = get_user_data(CLIENT_ID, ACCESS_TOKEN)
    if user_data:
        return user_data.get("id")
    return None


if __name__ == "__main__":
    from test_utils import test_util

    user_data = test_util(get_user_data, ["TWITCH_CLIENT_ID", "ACCESS_TOKEN"])
    if user_data:
        print(user_data)
