from dotenv import load_dotenv
from twitch_oauth import get_saved_twitch_tokens
from user_data import get_user_id
from os import getenv

load_dotenv()

def test_util(callback: callable, args: list, debug: bool = True, showEnv: bool = False):
    if debug:
        print("Testing utility function...")

    VAR_ENVIRONMENTS = []

    for arg in args:
        if arg == "ACCESS_TOKEN":
            VAR_ENVIRONMENTS.append(get_saved_twitch_tokens().get("access_token"))
        elif arg == "USER_ID":
            CLIENT_ID = getenv("TWITCH_CLIENT_ID")
            ACCESS_TOKEN = get_saved_twitch_tokens().get("access_token")
            VAR_ENVIRONMENTS.append(get_user_id(CLIENT_ID, ACCESS_TOKEN))
        elif getenv(arg):
            VAR_ENVIRONMENTS.append(getenv(arg))
        else:
            VAR_ENVIRONMENTS.append(arg)

    if debug and showEnv:
        print("VAR_ENVIRONMENTS:", VAR_ENVIRONMENTS)

    result = callback(*VAR_ENVIRONMENTS)

    return result