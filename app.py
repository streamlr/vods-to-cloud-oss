from dotenv import load_dotenv
from src.utils import server
import os

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

YT_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YT_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YT_REDIRECT_URI = os.getenv("YOUTUBE_REDIRECT_URI", "http://localhost:5000/yt/callback")


def main():
    server(
        CLIENT_ID,
        CLIENT_SECRET,
        REDIRECT_URI,
        YT_CLIENT_ID=YT_CLIENT_ID,
        YT_CLIENT_SECRET=YT_CLIENT_SECRET,
        YT_REDIRECT_URI=YT_REDIRECT_URI,
    )


if __name__ == "__main__":
    main()
