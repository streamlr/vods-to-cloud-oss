from flask import Flask, request, jsonify
from .twitch_oauth import get_auth_url, get_twitch_tokens_from_server, get_saved_twitch_tokens
from .webhook import register_webhook
from .user_data import get_user_data
from .get_vods import get_all_vods, get_latest_vod
from .vods_manager import VODDownloader, build_vod_url
import os

def server(CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str, PORT: int = 5000):
    app = Flask(__name__)
    
    # Initialize VOD downloader
    downloader = VODDownloader()

    def require_auth():
        """Check if user is authenticated"""
        tokens = get_saved_twitch_tokens()
        if not tokens:
            return None, jsonify({"error": "Authentication required"}), 401
        return tokens, None, None

    @app.route("/")
    def index():
        auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)

        if get_saved_twitch_tokens():
            logged_page_path = os.path.join("src", "pages", "logged.html")
            with open(logged_page_path, "r") as f:
                return f.read().replace("{{auth_url}}", auth_url)

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

    # VOD Management API Endpoints
    @app.route("/api/vods", methods=["GET"])
    def api_get_vods():
        """Get all VODs for the authenticated user"""
        tokens, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        try:
            user_data = get_user_data(CLIENT_ID, tokens["access_token"])
            if not user_data:
                return jsonify({"error": "Failed to get user data"}), 400
            
            vods = get_all_vods(CLIENT_ID, tokens["access_token"], user_data["id"])
            if vods is None:
                return jsonify({"error": "Failed to retrieve VODs"}), 400
                
            return jsonify({"vods": vods})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/vods/latest", methods=["GET"])
    def api_get_latest_vod():
        """Get the latest VOD for the authenticated user"""
        tokens, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        try:
            user_data = get_user_data(CLIENT_ID, tokens["access_token"])
            if not user_data:
                return jsonify({"error": "Failed to get user data"}), 400
            
            latest_vod = get_latest_vod(CLIENT_ID, tokens["access_token"], user_data["id"])
            if latest_vod is None:
                return jsonify({"error": "No VODs found"}), 404
                
            return jsonify({"vod": latest_vod})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/download/info/<vod_id>", methods=["GET"])
    def api_get_download_info(vod_id):
        """Get download info for a specific VOD"""
        tokens, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        try:
            vod_url = build_vod_url(vod_id)
            info = downloader.get_vod_info(vod_url)
            if info is None:
                return jsonify({"error": "Failed to get VOD info"}), 400
                
            return jsonify({"info": info})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/download/start", methods=["POST"])
    def api_start_download():
        """Start downloading a VOD"""
        tokens, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        data = request.get_json()
        if not data or 'vod_id' not in data:
            return jsonify({"error": "VOD ID is required"}), 400
        
        vod_id = data['vod_id']
        quality = data.get('quality', 'best')
        
        try:
            vod_url = build_vod_url(vod_id)
            
            # Start async download
            thread = downloader.download_vod_async(vod_url, quality)
            
            return jsonify({
                "message": "Download started",
                "vod_id": vod_id,
                "quality": quality,
                "thread_id": thread.ident
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/download/status/<vod_id>", methods=["GET"])
    def api_get_download_status(vod_id):
        """Get download status for a specific VOD"""
        tokens, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        try:
            status = downloader.get_download_status(vod_id)
            if status is None:
                return jsonify({"error": "Download not found"}), 404
                
            return jsonify({"status": status})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/download/status", methods=["GET"])
    def api_get_all_download_status():
        """Get status of all downloads"""
        tokens, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        try:
            all_status = downloader.get_all_download_status()
            return jsonify({"downloads": all_status})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/download/cancel/<vod_id>", methods=["POST"])
    def api_cancel_download(vod_id):
        """Cancel a download"""
        tokens, error_response, status_code = require_auth()
        if error_response:
            return error_response, status_code
        
        try:
            downloader.cancel_download(vod_id)
            return jsonify({"message": f"Download {vod_id} cancelled"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    app.run(port=PORT, debug=False, use_reloader=False)
