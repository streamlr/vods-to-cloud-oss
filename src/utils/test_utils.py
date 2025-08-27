from dotenv import load_dotenv
from twitch_oauth import get_saved_twitch_tokens
from os import getenv

load_dotenv()

def test_util(callback: callable, args: list, debug: bool = True, showEnv: bool = False):
    if debug:
        print("Testing utility function...")

    VAR_ENVIRONMENTS = []

    for arg in args:
        if arg == "ACCESS_TOKEN":
            VAR_ENVIRONMENTS.append(get_saved_twitch_tokens().get("access_token"))
        elif getenv(arg):
            VAR_ENVIRONMENTS.append(getenv(arg))
        else:
            VAR_ENVIRONMENTS.append(arg)

    if debug and showEnv:
        print("VAR_ENVIRONMENTS:", VAR_ENVIRONMENTS)

    result = callback(*VAR_ENVIRONMENTS)

    return result


def test_vod_download():
    """Test VOD download functionality"""
    from get_vods import get_latest_vod
    from vods_manager import VODDownloader, build_vod_url
    from user_data import get_user_data
    
    print("=== Testing VOD Download Functionality ===")
    
    # Get latest VOD
    print("\n1. Getting latest VOD...")
    try:
        latest_vod = test_util(get_latest_vod, ["TWITCH_CLIENT_ID", "ACCESS_TOKEN", "USER_ID"], debug=False)
        if not latest_vod:
            print("❌ No VODs found for testing")
            return False
            
        print(f"✅ Found VOD: {latest_vod['title']}")
        print(f"   ID: {latest_vod['id']}")
        print(f"   Duration: {latest_vod.get('duration', 'Unknown')}")
        print(f"   Views: {latest_vod.get('view_count', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error getting VOD: {e}")
        return False
    
    # Initialize downloader
    print("\n2. Initializing downloader...")
    try:
        downloader = VODDownloader(download_path="test_downloads")
        print("✅ Downloader initialized")
    except Exception as e:
        print(f"❌ Error initializing downloader: {e}")
        return False
    
    # Get VOD info
    print("\n3. Getting VOD download info...")
    try:
        vod_url = build_vod_url(latest_vod['id'])
        print(f"   VOD URL: {vod_url}")
        
        info = downloader.get_vod_info(vod_url)
        if not info:
            print("❌ Could not get VOD info")
            return False
            
        print("✅ VOD info retrieved:")
        print(f"   Title: {info.get('title', 'Unknown')}")
        print(f"   Uploader: {info.get('uploader', 'Unknown')}")
        print(f"   Duration: {info.get('duration', 'Unknown')} seconds")
        print(f"   Available formats: {len(info.get('formats', []))}")
        
    except Exception as e:
        print(f"❌ Error getting VOD info: {e}")
        return False
    
    # Add progress callback
    print("\n4. Setting up progress tracking...")
    def progress_callback(vod_id, status):
        if status.get('status') == 'downloading':
            downloaded = status.get('downloaded_bytes', 0)
            total = status.get('total_bytes', 0)
            if total > 0:
                percent = (downloaded / total) * 100
                speed = status.get('speed', 0)
                if speed:
                    speed_mb = speed / (1024 * 1024)
                    print(f"   Progress: {percent:.1f}% - Speed: {speed_mb:.1f} MB/s")
                else:
                    print(f"   Progress: {percent:.1f}%")
        elif status.get('status') == 'finished':
            print("   ✅ Download completed!")
        elif status.get('status') == 'error':
            print(f"   ❌ Download error: {status.get('error', 'Unknown error')}")
    
    downloader.add_progress_callback(progress_callback)
    print("✅ Progress tracking configured")
    
    # Test download (dry run - just show what would happen)
    print("\n5. Testing download capability (info only)...")
    print("   NOTE: Actual download not performed in test")
    print(f"   Would download: {info.get('title')}")
    print(f"   Quality: 720p")
    print(f"   Output directory: test_downloads/")
    print(f"   Filename pattern: {info.get('uploader')} - {info.get('title')} - {latest_vod['id']}")
    
    # Test async download status tracking
    print("\n6. Testing download status tracking...")
    try:
        # Simulate a download entry
        vod_id = latest_vod['id']
        downloader.current_downloads[vod_id] = {
            'vod_id': vod_id,
            'title': latest_vod['title'],
            'url': vod_url,
            'status': 'testing',
            'start_time': '2024-01-01T00:00:00'
        }
        
        status = downloader.get_download_status(vod_id)
        if status:
            print("✅ Status tracking working:")
            print(f"   VOD ID: {status['vod_id']}")
            print(f"   Status: {status['status']}")
            print(f"   Title: {status['title']}")
        else:
            print("❌ Status tracking failed")
            
        all_status = downloader.get_all_download_status()
        print(f"✅ All downloads tracking: {len(all_status)} entries")
        
    except Exception as e:
        print(f"❌ Error in status tracking: {e}")
        return False
    
    print("\n=== VOD Download Test Completed Successfully ===")
    print("Note: To perform actual downloads, use the download methods directly")
    print("Example: downloader.download_vod(vod_url, quality='720p')")
    return True


if __name__ == "__main__":
    # Run the VOD download test
    test_vod_download()