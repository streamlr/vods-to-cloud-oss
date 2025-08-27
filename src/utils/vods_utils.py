import yt_dlp


def get_vod_url(VOD_ID: str) -> str:
    return f"https://www.twitch.tv/videos/{VOD_ID}"


def download_vods(VOD_ID: str, ACCESS_TOKEN: str | None) -> bool:
    VOD_URL = get_vod_url(VOD_ID)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'vod.mp4',
        'http_headers': headers if ACCESS_TOKEN else {},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([VOD_URL])
            return True
    except Exception as _:
        return False
    
if __name__ == "__main__":
    from test_utils import test_util

    test_status = test_util(download_vods, ["2548950092", "ACCESS_TOKEN"])
    print(f"Test status: {test_status}")
