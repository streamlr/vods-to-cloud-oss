import urllib.parse
import requests

def get_code_verifier(CLIENT_ID: str, REDIRECT_URI: str):
    scope = ["user:read:broadcast"]
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scope)
    }

    url = f"https://id.twitch.tv/oauth2/authorize?{urllib.parse.urlencode(params)}"
    print("Visit this URL for authorization:", url)

    code_verifier = input("Enter the code from the URL: ")

    return code_verifier


def twitch_oauth(CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str):
    if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
        print("Missing required environment variables.")
        return None

    code_verifier = get_code_verifier(CLIENT_ID, REDIRECT_URI)

    print(code_verifier)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv("./.env")

    CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

    response = twitch_oauth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    print(response)
