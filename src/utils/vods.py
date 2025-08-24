import requests


def get_all_vods(CLIENT_ID: str, ACCESS_TOKEN: str):
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get("https://api.twitch.tv/helix/videos", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve VODs:", response.status_code, response.text)
        return None


def get_new_vod(CLIENT_ID: str, ACCESS_TOKEN: str):
    all_vods = get_all_vods(CLIENT_ID, ACCESS_TOKEN)


if __name__ == "__main__":
    from sys import argv

    CLIENT_ID = argv[1]
    ACCESS_TOKEN = argv[2]

    print(get_all_vods(CLIENT_ID, ACCESS_TOKEN))
