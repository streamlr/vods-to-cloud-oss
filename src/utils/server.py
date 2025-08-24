from flask import Flask, request
from .twitch_oauth import get_auth_url, get_twitch_tokens_from_server, get_saved_twitch_tokens
from .webhook import register_webhook
from .user_data import get_user_data
import os

def server(CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str, PORT: int = 5000):
    app = Flask(__name__)


    @app.route("/")
    def index():
        auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)

        if get_saved_twitch_tokens():
            logged_page_path = os.path.join("src", "pages", "logged.html")
            with open(logged_page_path, "r") as f:
                return f.read()

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

        user_data = get_user_data(CLIENT_ID, tokens["access_token"])

        register_webhook(CLIENT_ID, tokens["access_token"], user_data["id"], f"http://127.0.0.1:{PORT}/webhook")

        callback_page_path = os.path.join("src", "pages", "callback.html")
        with open(callback_page_path, "r") as f:
            return f.read()

        return "Login successful, you can close this tab now."


    @app.route("/webhook", methods=["POST"])
    def webhook():
        data = request.json

        print("Received webhook:", data)

        return "Webhook received", 200


    app.run(port=PORT, debug=False, use_reloader=False)
