from flask import Flask, request, redirect
from .twitch_oauth import get_auth_url, get_twitch_tokens_from_server, get_saved_twitch_tokens
from .webhook import register_webhook
from .user_data import get_user_data
import os
from .youtube_oauth import (
    yt_get_auth_url,
    yt_exchange_code_for_tokens,
    yt_get_saved_tokens as yt_get_saved_tokens,
    yt_get_valid_access_token,
)

def server(
    CLIENT_ID: str,
    CLIENT_SECRET: str,
    REDIRECT_URI: str,
    PORT: int = 5000,
    YT_CLIENT_ID: str | None = None,
    YT_CLIENT_SECRET: str | None = None,
    YT_REDIRECT_URI: str | None = None,
):
    app = Flask(__name__)


    @app.route("/")
    def index():
        twitch_auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)

        # YouTube session status and button behavior
        if YT_CLIENT_ID and YT_CLIENT_SECRET and YT_REDIRECT_URI:
            yt_token = yt_get_valid_access_token(YT_CLIENT_ID, YT_CLIENT_SECRET)
            yt_status = "YouTube session: Active" if yt_token else "YouTube session: Not connected"
            if yt_token:
                youtube_button_text = "YouTube connected"
                youtube_button_href = "/"
            else:
                youtube_button_text = "Login with YouTube"
                youtube_button_href = yt_get_auth_url(YT_CLIENT_ID, YT_REDIRECT_URI)
        else:
            yt_status = "YouTube auth not configured"
            youtube_button_text = "YouTube not configured"
            youtube_button_href = "#"

        # YouTube session status
        if YT_CLIENT_ID and YT_CLIENT_SECRET:
            yt_token = yt_get_valid_access_token(YT_CLIENT_ID, YT_CLIENT_SECRET)
            yt_status = "YouTube session: Active" if yt_token else "YouTube session: Not connected"
        else:
            yt_status = "YouTube auth not configured"

        # If either Twitch or YouTube session is active, show logged page
        if get_saved_twitch_tokens() or ("Active" in yt_status):
            logged_page_path = os.path.join("src", "pages", "logged.html")
            with open(logged_page_path, "r") as f:
                return (
                    f.read()
                    .replace("{{twitch_auth_url}}", twitch_auth_url)
                    .replace("{{youtube_button_href}}", youtube_button_href)
                    .replace("{{youtube_button_text}}", youtube_button_text)
                    .replace("{{yt_status}}", yt_status)
                )

        login_page_path = os.path.join("src", "pages", "login.html")
        with open(login_page_path, "r") as f:
            return (
                f.read()
                .replace("{{twitch_auth_url}}", twitch_auth_url)
                .replace("{{youtube_button_href}}", youtube_button_href)
                .replace("{{youtube_button_text}}", youtube_button_text)
                .replace("{{yt_status}}", yt_status)
            )


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


    # --- YouTube OAuth routes ---
    @app.route("/yt")
    def yt_index():
        if not (YT_CLIENT_ID and YT_REDIRECT_URI):
            return "YouTube auth is not configured.", 500

        twitch_auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)

        # YouTube session status and button behavior
        yt_token = yt_get_valid_access_token(YT_CLIENT_ID, YT_CLIENT_SECRET)
        yt_status = "YouTube session: Active" if yt_token else "YouTube session: Not connected"
        if yt_token:
            youtube_button_text = "YouTube connected"
            youtube_button_href = "/"
        else:
            youtube_button_text = "Login with YouTube"
            youtube_button_href = yt_get_auth_url(YT_CLIENT_ID, YT_REDIRECT_URI)

        # YouTube session status
        if YT_CLIENT_ID and YT_CLIENT_SECRET:
            yt_token = yt_get_valid_access_token(YT_CLIENT_ID, YT_CLIENT_SECRET)
            yt_status = "YouTube session: Active" if yt_token else "YouTube session: Not connected"
        else:
            yt_status = "YouTube auth not configured"

        # If already have saved tokens, still show logged page allowing re-login
        if yt_get_saved_tokens():
            logged_page_path = os.path.join("src", "pages", "logged.html")
            with open(logged_page_path, "r") as f:
                return (
                    f.read()
                    .replace("{{twitch_auth_url}}", twitch_auth_url)
                    .replace("{{youtube_button_href}}", youtube_button_href)
                    .replace("{{youtube_button_text}}", youtube_button_text)
                    .replace("{{yt_status}}", yt_status)
                )

        login_page_path = os.path.join("src", "pages", "login.html")
        with open(login_page_path, "r") as f:
            return (
                f.read()
                .replace("{{twitch_auth_url}}", twitch_auth_url)
                .replace("{{youtube_button_href}}", youtube_button_href)
                .replace("{{youtube_button_text}}", youtube_button_text)
                .replace("{{yt_status}}", yt_status)
            )


    @app.route("/yt/callback")
    def yt_callback():
        if not (YT_CLIENT_ID and YT_CLIENT_SECRET and YT_REDIRECT_URI):
            return "YouTube auth is not configured.", 500

        code = request.args.get("code")
        if not code:
            return "Error: no code received", 400

        yt_exchange_code_for_tokens(YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REDIRECT_URI, code)

        callback_page_path = os.path.join("src", "pages", "callback.html")
        with open(callback_page_path, "r") as f:
            return f.read()


    @app.route("/yt/logout")
    def yt_logout():
        """Revoke YouTube token (if any) and delete local token file."""
        yt_path = os.path.join("src", "data", "yt_tokens.json")
        try:
            tokens = yt_get_saved_tokens()
            if tokens and (token := tokens.get("access_token") or tokens.get("refresh_token")):
                import requests

                # Google recommends sending token in body as x-www-form-urlencoded
                requests.post(
                    "https://oauth2.googleapis.com/revoke",
                    data={"token": token},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10,
                )
        except Exception:
            pass

        # Remove local tokens regardless of remote revoke result
        try:
            if os.path.exists(yt_path):
                os.remove(yt_path)
        except Exception:
            pass

        return redirect("/")


    @app.route("/webhook", methods=["POST"])
    def webhook():
        data = request.json

        print("Received webhook:", data)

        return "Webhook received", 200


    @app.route("/twitch/logout")
    def twitch_logout():
        """Revoke Twitch token (if any) and delete local token file."""
        twitch_path = os.path.join("src", "data", "tokens.json")
        try:
            tokens = get_saved_twitch_tokens()
            if tokens and (token := tokens.get("access_token")):
                import requests

                requests.post(
                    "https://id.twitch.tv/oauth2/revoke",
                    params={"client_id": CLIENT_ID, "token": token},
                    timeout=10,
                )
        except Exception:
            pass

        try:
            if os.path.exists(twitch_path):
                os.remove(twitch_path)
        except Exception:
            pass

        return redirect("/")


    app.run(port=PORT, debug=False, use_reloader=False)


if __name__ == "__main__":
    from test_utils import test_util

    test_util(server, ["TWITCH_CLIENT_ID", "TWITCH_CLIENT_SECRET", "TWITCH_REDIRECT_URI", 5000])
