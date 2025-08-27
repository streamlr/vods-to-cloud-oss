import yt_dlp


def get_vod_url(VOD_ID: str) -> str:
    return f"https://www.twitch.tv/videos/{VOD_ID}"


def download_vods(ACCESS_TOKEN: str, VOD_ID: str) -> bool:
    VOD_URL = get_vod_url(VOD_ID)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'vod.mp4',
        'http_headers': headers
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([VOD_URL])
            return True
    except Exception as _:
        return False
