from dotenv import load_dotenv
from flask import Flask, request
from src.utils import get_auth_url, get_twitch_tokens_from_server
import time
import os
import threading


tokens = None
app = Flask(__name__)


def shutdown_server():
    try:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError("Cannot shutdown server")
        func()
    except Exception as e:
        pass


@app.route("/")
def index():
    auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)
    return f'<a href="{auth_url}">Login with Twitch</a>'


@app.route("/callback")
def callback():
    global tokens

    code = request.args.get("code")
    if not code:
        return "Error: no code received", 400

    tokens = get_twitch_tokens_from_server(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, code)

    shutdown_server()
    return "Login successful, you can close this tab now."


def run_server():
    app.run(port=5000, debug=False, use_reloader=False)


def auth_server(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI):
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    while not tokens:
        time.sleep(1)

    return tokens


if __name__ == "__main__":
    load_dotenv()

    CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

    result = auth_server(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    print("Tokens received:", result)
