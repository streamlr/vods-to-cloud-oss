from ..utils import auth_server


def twitch_oauth(CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str):
    if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
        print("Missing required environment variables.")
        return None

    auth_server(CLIENT_ID, REDIRECT_URI)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv("./.env")

    CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

    response = twitch_oauth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    print(response)
