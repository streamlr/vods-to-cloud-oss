import yt_dlp
import os
from typing import Optional, Dict


def download_vod(vod_url: str, output_dir: str = "downloads", vod_info: Optional[Dict] = None) -> bool:
    """
    Download a VOD using yt-dlp

    Args:
        vod_url: VOD's URL from Twitch
        output_dir: Directory to savew the file
        vod_info: Additional VOD information

    Returns:
        True if the download was successful, False otherwise
    """
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Configuration for yt-dlp
    ydl_opts = {
          'outtmpl': os.path.join(output_dir, '%(title)s-%(id)s.%(ext)s'),
          'format': 'best',  # Download the best quality available
          'noplaylist': True,  # Only download the individual video
      }

    try:
        with yt_dlp as ydl:
            print(f"Starting download of: {vod_url}")
            ydl.download([vod_url])
            print("Download completed successfully")
            return True
    
    except Exception as e:
        print(f"Error during download: {str(e)}")
        return False
    
def get_vod_info_with_yt_dlp(vod_url: str) -> Optional[Dict]:
    """
    Get VOD information without downloading it
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(vod_url, download=False)
            return {
                'title': info.get('title'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'upload_date': info.get('upload_date'),
                'view_count': info.get('view_count'),
                'description': info.get('description'),
            }
    except Exception as e:
        print(f"Error getting VOD information: {str(e)}")

def download_vod_from_id(vod_id: str, output_dir: str = "downloads") -> bool:
    """
    Download a VOD using your Twitch ID
    """
    vod_url = f"https://www.twitch.tv/videos/{vod_id}"
    return download_vod(vod_url, output_dir)


if __name__ == "__main__":
    # Example of use
    test_vod_id = "123456789"  # Replace with real ID
    success = download_vod_from_id(test_vod_id)
    print(f"Download {'successful' if success else 'failed'}")