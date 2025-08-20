from dotenv import load_dotenv
from src.utils import get_saved_twitch_tokens
from auth_server import auth_server
import os
import time

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")


def main():
    tokens = auth_server(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    print("Tokens received:", tokens)


if __name__ == "__main__":
    main()
