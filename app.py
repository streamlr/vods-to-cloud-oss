from dotenv import load_dotenv
from src.utils import server
import os

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")


def main():
    server(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)


if __name__ == "__main__":
    main()
