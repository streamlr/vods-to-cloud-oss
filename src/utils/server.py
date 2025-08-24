from flask import Flask, request
from src.utils import get_auth_url, get_twitch_tokens_from_server, register_webhook
import os


def server(CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str):
    app = Flask(__name__)


    @app.route("/")
    def index():
        auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)

        login_page_path = os.path.join("src", "pages", "login.html")
        with open(login_page_path, "r") as f:
            return f.read().replace("{{auth_url}}", auth_url)

        return f"<a href=\"{auth_url}\">Login with Twitch</a>"


    @app.route("/callback")
    def callback():
        code = request.args.get("code")
        if not code:
            return "Error: no code received", 400

        tokens = get_twitch_tokens_from_server(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, code)

        register_webhook(tokens)

        callback_page_path = os.path.join("src", "pages", "callback.html")
        with open(callback_page_path, "r") as f:
            return f.read()

        return "Login successful, you can close this tab now."


    @app.route("/webhook", methods=["POST"])
    def webhook():
        data = request.json

        print("Received webhook:", data)

        return "Webhook received", 200


    app.run(port=5000, debug=False, use_reloader=False)
