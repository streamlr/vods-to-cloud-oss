import requests


def delete_vod_by_id(CLIENT_ID: str, ACCESS_TOKEN: str, VOD_ID: str):
    url = f"https://api.twitch.tv/helix/videos"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "id": VOD_ID
    }

    response = requests.delete(url, headers=headers, params=params)

    return response.json()


if __name__ == "__main__":
    from test_utils import test_util

    response = test_util(delete_vod_by_id, ["TWITCH_CLIENT_ID", "ACCESS_TOKEN", "2548963347"])
    print("Response:", response)
