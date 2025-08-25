import requests
from typing import List, Dict, Optional


def get_user_videos(CLIENT_ID: str, ACCESS_TOKEN: str, user_id: str, limit: int = 5) -> List[Dict]:
    """
    Gets the user's VOD list from the Twitch API
    """
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "user_id": user_id,
        "type": "archive", # Only VODs are admissible
        "first": limit
    }

    response = requests.get("https://api.twitch.tv/helix/videos", headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error getting videos: {response.status_code}, {response.text}")
        return []
    
def get_latest_vod(CLIENT_ID: str, ACCESS_TOKEN: str, user_id: str) -> Optional[Dict]:
    """
    Gets the user's latest VOD
    """
    videos = get_user_videos(CLIENT_ID, ACCESS_TOKEN, user_id, limit=1)
    return videos[0] if videos else None

def print_vod_info(vod: Dict):
    """
    Print basic VOD information for debugging
    """
    if vod:
        print(f"VOD ID: {vod['id']}")
        print(f"Título: {vod['title']}")
        print(f"URL: {vod['url']}")
        print(f"Duración: {vod['duration']}")
        print(f"Creado: {vod['created_at']}")
    else:
        print("No VOD available")
