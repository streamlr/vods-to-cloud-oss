import os
import mimetypes
import requests
from .youtube_oauth import yt_get_valid_access_token
from typing import Optional



def upload_to_youtube(
    file_path: str,
    title: str,
    description: str = "",
    tags: Optional[list[str]] = None,
    privacy_status: str = "private",
    made_for_kids: bool = False,
    yt_client_id: Optional[str] = None,
    yt_client_secret: Optional[str] = None,
) -> dict:
    """Uploads a video to YouTube using a resumable upload session.

    Returns the API response JSON on success.
    """
    yt_client_id = yt_client_id or os.getenv("YOUTUBE_CLIENT_ID")
    yt_client_secret = yt_client_secret or os.getenv("YOUTUBE_CLIENT_SECRET")

    if not yt_client_id or not yt_client_secret:
        raise RuntimeError("YouTube client credentials are not configured.")

    access_token = yt_get_valid_access_token(yt_client_id, yt_client_secret)
    if not access_token:
        raise RuntimeError("No valid YouTube access token. Please login at /yt.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    file_size = os.path.getsize(file_path)
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = "application/octet-stream"

    # 1) Initiate resumable upload session
    init_url = (
        "https://www.googleapis.com/upload/youtube/v3/videos"
        "?uploadType=resumable&part=snippet,status"
    )
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Upload-Content-Type": content_type,
        "X-Upload-Content-Length": str(file_size),
        "Content-Type": "application/json; charset=UTF-8",
    }
    body = {
        "snippet": {
            "title": title,
            "description": description or "",
        },
        "status": {
            "privacyStatus": privacy_status,
            # Set audience selection so Studio doesn't prompt
            "selfDeclaredMadeForKids": bool(made_for_kids),
        },
    }
    if tags:
        body["snippet"]["tags"] = tags

    init_resp = requests.post(init_url, headers=headers, json=body)
    if init_resp.status_code not in (200, 201):
        raise RuntimeError(f"Failed to start upload: {init_resp.status_code} {init_resp.text}")

    upload_url = init_resp.headers.get("Location")
    if not upload_url:
        raise RuntimeError("Upload session URL not provided by API.")

    # 2) Upload the file in a single request (non-chunked)
    with open(file_path, "rb") as f:
        upload_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Length": str(file_size),
            "Content-Type": content_type,
        }
        put_resp = requests.put(upload_url, headers=upload_headers, data=f)

    if put_resp.status_code not in (200, 201):
        raise RuntimeError(f"Upload failed: {put_resp.status_code} {put_resp.text}")

    return put_resp.json()


if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv
    import json as _json

    parser = argparse.ArgumentParser(description="Upload a video to YouTube")
    parser.add_argument("--file", required=True, help="Path to the video file")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", default="", help="Video description")
    parser.add_argument(
        "--tags",
        default="",
        help="Comma-separated list of tags (e.g., tag1,tag2)",
    )
    parser.add_argument(
        "--privacy",
        choices=["public", "unlisted", "private"],
        default="unlisted",
        help="Privacy status",
    )
    parser.add_argument(
        "--made-for-kids",
        action="store_true",
        help="Mark video as made for kids (default: not for kids)",
    )
    parser.add_argument("--yt-client-id", default=None, help="Override YouTube client ID")
    parser.add_argument("--yt-client-secret", default=None, help="Override YouTube client secret")

    args = parser.parse_args()

    load_dotenv()

    tags_list = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else None

    try:
        resp = upload_to_youtube(
            file_path=args.file,
            title=args.title,
            description=args.description,
            tags=tags_list,
            privacy_status=args.privacy,
            made_for_kids=bool(args.made_for_kids),
            yt_client_id=args.yt_client_id,
            yt_client_secret=args.yt_client_secret,
        )
        print(_json.dumps(resp, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)
