from dotenv import load_dotenv
from src.utils import get_saved_twitch_tokens, get_access_token_from_refresh
from auth_server import auth_server
import json
import os
import time
import schedule

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

tokens = None


def update_token():
    global tokens

    REFRESH_TOKEN = tokens.get("refresh_token")

    tokens = get_access_token_from_refresh(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)


def main():
    global tokens

    tokens = auth_server()

    # schedule.every(1).hours.do(update_token)

    while True:
        # schedule.run_pending()

        print(tokens)

        time.sleep(1)


if __name__ == "__main__":
    main()
