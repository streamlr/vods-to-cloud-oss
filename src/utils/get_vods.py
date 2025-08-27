from datetime import datetime
import requests


def get_all_vods(CLIENT_ID: str, ACCESS_TOKEN: str, USER_ID: str):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Client-ID": CLIENT_ID,
    }

    params = {
        "user_id": USER_ID,
        "type": "archive",
    }

    response = requests.get("https://api.twitch.tv/helix/videos", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['data']
    else:
        print("Failed to retrieve VODs:", response.status_code, response.text)
        return None



def get_latest_vod(CLIENT_ID: str, ACCESS_TOKEN: str, USER_ID: str):
    all_vods = get_all_vods(CLIENT_ID, ACCESS_TOKEN, USER_ID)
    
    if all_vods:
        latest_vod = max(
            all_vods,
            key=lambda vod: datetime.fromisoformat(vod['created_at'].replace("Z", "+00:00"))
        )
        return latest_vod
    
    return None


if __name__ == "__main__":
    from test_utils import test_util
    from user_data import get_user_data

    vod_data = test_util(get_all_vods, ["TWITCH_CLIENT_ID", "ACCESS_TOKEN", "USER_ID"])
    print("VODs retrieved:", vod_data)

    latest_vod_data = test_util(get_latest_vod, ["TWITCH_CLIENT_ID", "ACCESS_TOKEN", "USER_ID"])
    print("Latest VOD data:", latest_vod_data)
