import requests


def hide_vod_by_id(CLIENT_ID: str, ACCESS_TOKEN: str, VOD_ID: str):
    url = f"https://api.twitch.tv/helix/videos/{VOD_ID}"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    data = {
        "viewable": "private"
    }

    resp = requests.patch(url, headers=headers, json=data)

    return resp.json()


if __name__ == "__main__":
    from test_utils import test_util

    response = test_util(hide_vod_by_id, ["TWITCH_CLIENT_ID", "ACCESS_TOKEN", "VOD_ID"])
    print("Response:", response)
