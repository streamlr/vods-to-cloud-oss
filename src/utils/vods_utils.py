from os import path, makedirs, getcwd
import subprocess

# This script uses twitch-dlp to download Twitch VODs. But it only supports public vods.

COOKIE_PATH = path.join(getcwd(), "cookies.txt")
VODS_DIR_PATH = "vods"


def get_vod_url(VOD_ID: str) -> str:
    return f"https://www.twitch.tv/videos/{VOD_ID}"


def download_vods(VOD_ID: str, ACCESS_TOKEN: str | None) -> bool:
    VOD_URL = get_vod_url(VOD_ID)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    makedirs(VODS_DIR_PATH, exist_ok=True)

    OUTPUT_PATH = path.join(VODS_DIR_PATH, f"{VOD_ID}.mp4")

    flags = [
        "-q", "source",
        "-o", OUTPUT_PATH,
    ]

    try:
        subprocess.run([
            "twitch-dl", "download", VOD_URL, *flags
        ], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    from test_utils import test_util

    test_status = test_util(download_vods, ["2548950092", "ACCESS_TOKEN"])
    print(f"Test status: {test_status}")
