import requests
import yt_dlp
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Callable
import threading


def delete_vod_by_id(CLIENT_ID: str, ACCESS_TOKEN: str, VOD_ID: str):
    url = f"https://api.twitch.tv/helix/videos"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "id": VOD_ID
    }

    response = requests.delete(url, headers=headers, params=params)

    return response.json()


class VODDownloader:
    def __init__(self, download_path: str = "downloads"):
        self.download_path = download_path
        self.progress_callbacks: List[Callable] = []
        self.current_downloads: Dict[str, dict] = {}
        
        os.makedirs(download_path, exist_ok=True)
    
    def add_progress_callback(self, callback: Callable):
        """Add callback to monitor download progress"""
        self.progress_callbacks.append(callback)
    
    def _progress_hook(self, d: dict):
        """Internal hook to handle yt-dlp progress"""
        vod_id = d.get('info_dict', {}).get('id', 'unknown')
        
        if vod_id in self.current_downloads:
            self.current_downloads[vod_id].update({
                'status': d['status'],
                'downloaded_bytes': d.get('downloaded_bytes', 0),
                'total_bytes': d.get('total_bytes', 0),
                'speed': d.get('speed', 0),
                'eta': d.get('eta', 0),
                'filename': d.get('filename', ''),
                'last_update': datetime.now().isoformat()
            })
        
        # Notify registered callbacks
        for callback in self.progress_callbacks:
            try:
                callback(vod_id, self.current_downloads.get(vod_id, {}))
            except Exception as e:
                print(f"Error in progress callback: {e}")
    
    def get_vod_info(self, vod_url: str) -> Optional[dict]:
        """Get VOD information without downloading it"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(vod_url, download=False)
                return {
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'uploader': info.get('uploader'),
                    'duration': info.get('duration'),
                    'view_count': info.get('view_count'),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description'),
                    'thumbnail': info.get('thumbnail'),
                    'formats': [f for f in info.get('formats', []) if f.get('vcodec') != 'none']
                }
        except Exception as e:
            print(f"Error getting VOD info: {e}")
            return None
    
    def download_vod(self, vod_url: str, quality: str = 'best', 
                     filename_template: str = None) -> bool:
        """
        Download a Twitch VOD
        
        Args:
            vod_url: Twitch VOD URL
            quality: Video quality ('best', 'worst', '720p', etc.)
            filename_template: Template for filename
        
        Returns:
            bool: True if download was successful
        """
        if not filename_template:
            filename_template = '%(uploader)s - %(title)s - %(id)s.%(ext)s'
        
        ydl_opts = {
            'format': quality,
            'outtmpl': os.path.join(self.download_path, filename_template),
            'progress_hooks': [self._progress_hook],
            'writeinfojson': True,  # Save metadata as JSON
            'writethumbnail': True,  # Download thumbnail
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get info first for tracking
                info = ydl.extract_info(vod_url, download=False)
                vod_id = info.get('id')
                
                # Initialize tracking
                self.current_downloads[vod_id] = {
                    'vod_id': vod_id,
                    'title': info.get('title'),
                    'url': vod_url,
                    'status': 'starting',
                    'start_time': datetime.now().isoformat()
                }
                
                # Download
                ydl.download([vod_url])
                
                # Mark as completed
                if vod_id in self.current_downloads:
                    self.current_downloads[vod_id]['status'] = 'finished'
                    self.current_downloads[vod_id]['end_time'] = datetime.now().isoformat()
                
                return True
                
        except Exception as e:
            print(f"Error downloading VOD: {e}")
            vod_id = vod_url.split('/')[-1]
            if vod_id in self.current_downloads:
                self.current_downloads[vod_id]['status'] = 'error'
                self.current_downloads[vod_id]['error'] = str(e)
            return False
    
    def download_vod_async(self, vod_url: str, quality: str = 'best',
                          filename_template: str = None) -> threading.Thread:
        """Download a VOD asynchronously"""
        thread = threading.Thread(
            target=self.download_vod,
            args=(vod_url, quality, filename_template)
        )
        thread.start()
        return thread
    
    def get_download_status(self, vod_id: str) -> Optional[dict]:
        """Get download status for a specific VOD"""
        return self.current_downloads.get(vod_id)
    
    def get_all_download_status(self) -> dict:
        """Get status of all downloads"""
        return self.current_downloads.copy()
    
    def cancel_download(self, vod_id: str):
        """Cancel a download (limited by yt-dlp capabilities)"""
        if vod_id in self.current_downloads:
            self.current_downloads[vod_id]['status'] = 'cancelled'


def build_vod_url(vod_id: str) -> str:
    """Build VOD URL from ID"""
    return f"https://www.twitch.tv/videos/{vod_id}"


if __name__ == "__main__":
    from test_utils import test_util
    from get_vods import get_latest_vod
    
    # Test VOD deletion
    response = test_util(delete_vod_by_id, ["TWITCH_CLIENT_ID", "ACCESS_TOKEN", "2548963347"])
    print("Delete Response:", response)
    
    # Test VOD download
    def test_download():
        latest_vod = test_util(get_latest_vod, ["TWITCH_CLIENT_ID", "ACCESS_TOKEN", "USER_ID"])
        if latest_vod:
            vod_url = build_vod_url(latest_vod['id'])
            print(f"Testing download of: {latest_vod['title']}")
            print(f"URL: {vod_url}")
            
            downloader = VODDownloader()
            
            # Progress callback to show download progress
            def progress_callback(vod_id, status):
                if status.get('status') == 'downloading':
                    downloaded = status.get('downloaded_bytes', 0)
                    total = status.get('total_bytes', 0)
                    if total > 0:
                        percent = (downloaded / total) * 100
                        print(f"Progress: {percent:.1f}%")
            
            downloader.add_progress_callback(progress_callback)
            
            # Get info first
            info = downloader.get_vod_info(vod_url)
            print(f"VOD Info: {info}")
            
            # Download with 720p quality
            success = downloader.download_vod(vod_url, quality='720p')
            print(f"Download successful: {success}")
        else:
            print("No VODs found to test download")
    
    # Uncomment to test download
    # test_download()
