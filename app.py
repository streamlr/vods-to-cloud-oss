from dotenv import load_dotenv
from src.utils import get_twitch_tokens
import os

load_dotenv()


def main():
    CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

    tokens = get_twitch_tokens(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    print(tokens)


if __name__ == "__main__":
    main()
