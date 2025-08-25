from dotenv import load_dotenv
from twitch_oauth import get_saved_twitch_tokens
from os import getenv

load_dotenv()

def test_util(callback: callable, args: list):
    VAR_ENVIRONMENTS = []

    for arg in args:
        if arg == "ACCESS_TOKEN":
            VAR_ENVIRONMENTS.append(get_saved_twitch_tokens().get("access_token"))
        elif getenv(arg):
            VAR_ENVIRONMENTS.append(getenv(arg))
        else:
            VAR_ENVIRONMENTS.append(arg)

    result = callback(*VAR_ENVIRONMENTS)

    return result