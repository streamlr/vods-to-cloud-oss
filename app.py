from dotenv import load_dotenv
from src.lib import twitch_oauth
import os

load_dotenv()


def main():
    CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

    response = twitch_oauth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    print(response)


if __name__ == "__main__":
    main()
