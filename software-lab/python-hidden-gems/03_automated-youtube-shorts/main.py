"""
Project 03: Automated YouTube Shorts

Hidden Gem: `yt-dlp` — the most powerful YouTube downloader (fork of youtube-dl).

What it does: Downloads a YouTube video and extracts the first 60 seconds
as a short clip. Demonstrates yt-dlp's metadata extraction and format selection.
"""
import os
import subprocess
import json


def get_video_info(url):
    """Fetch video metadata using yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-download", url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
    except FileNotFoundError:
        print("yt-dlp not installed. Install with: pip install yt-dlp")
    except subprocess.TimeoutExpired:
        print("Timed out fetching video info.")
    except Exception as e:
        print(f"Error: {e}")
    return None


def download_clip(url, output_path="clip.mp4", max_duration=60):
    """Download first N seconds of a video."""
    cmd = [
        "yt-dlp",
        "-f", "best[height<=720]",
        "--download-sections", f"*0-{max_duration}",
        "--force-keyframes-at-cuts",
        "-o", output_path,
        url
    ]
    try:
        print(f"Downloading first {max_duration}s of: {url}")
        subprocess.run(cmd, check=True)
        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"Clip saved: {output_path} ({size_mb:.1f} MB)")
            return True
    except FileNotFoundError:
        print("yt-dlp not installed. Install with: pip install yt-dlp")
    except subprocess.CalledProcessError as e:
        print(f"Download failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return False


def main():
    # Use a well-known public domain video for demo
    url = "https://www.youtube.com/watch?v=BaW_jenozKc"  # Big Buck Bunny

    print("--- YouTube Shorts Extractor ---")
    print(f"URL: {url}")

    info = get_video_info(url)
    if info:
        print(f"Title: {info.get('title', 'Unknown')}")
        print(f"Duration: {info.get('duration', 'Unknown')}s")
        print(f"Uploader: {info.get('uploader', 'Unknown')}")
        print(f"Views: {info.get('view_count', 'Unknown'):,}")

    print()
    success = download_clip(url, max_duration=30)
    if not success:
        print("\nDemo mode: yt-dlp is required to download videos.")
        print("Install it with: pip install yt-dlp")


if __name__ == "__main__":
    main()
