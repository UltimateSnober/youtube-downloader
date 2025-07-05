import os
import sys
import argparse
from pathlib import Path
import yt_dlp
from urllib.parse import urlparse, parse_qs


class YouTubeDownloader:
    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def get_video_info(self, url):
        """Get video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

    def download_video(self, url, quality="best", audio_only=False):
        """Download a single video"""
        if audio_only:
            format_selector = 'bestaudio/best'
            outtmpl = str(self.output_dir / '%(title)s.%(ext)s')
        else:
            if quality == "best":
                format_selector = 'best'
            elif quality == "worst":
                format_selector = 'worst'
            else:
                format_selector = f'best[height<={quality}]'
            outtmpl = str(self.output_dir / '%(title)s.%(ext)s')

        ydl_opts = {
            'format': format_selector,
            'outtmpl': outtmpl,
            'noplaylist': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading: {url}")
                ydl.download([url])
                print("Download completed successfully!")
                return True
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False

    def download_playlist(self, url, quality="best", audio_only=False, max_downloads=None):
        """Download entire playlist"""
        if audio_only:
            format_selector = 'bestaudio/best'
            outtmpl = str(self.output_dir /
                          '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s')
        else:
            if quality == "best":
                format_selector = 'best'
            elif quality == "worst":
                format_selector = 'worst'
            else:
                format_selector = f'best[height<={quality}]'
            outtmpl = str(self.output_dir /
                          '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s')

        ydl_opts = {
            'format': format_selector,
            'outtmpl': outtmpl,
            'ignoreerrors': True,
        }

        if max_downloads:
            ydl_opts['playlistend'] = max_downloads

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading playlist: {url}")
                ydl.download([url])
                print("Playlist download completed!")
                return True
        except Exception as e:
            print(f"Error downloading playlist: {e}")
            return False

    def is_playlist(self, url):
        """Check if URL is a playlist"""
        parsed_url = urlparse(url)
        if 'playlist' in parsed_url.query:
            return True
        if '/playlist' in parsed_url.path:
            return True
        return False

    def list_formats(self, url):
        """List available formats for a video"""
        ydl_opts = {
            'listformats': True,
            'quiet': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Error listing formats: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='YouTube Video/Playlist Downloader')
    parser.add_argument('url', help='YouTube video or playlist URL')
    parser.add_argument('-o', '--output', default='downloads',
                        help='Output directory (default: downloads)')
    parser.add_argument('-q', '--quality', default='best',
                        help='Video quality: best, worst, or height (e.g., 720, 1080)')
    parser.add_argument('-a', '--audio-only', action='store_true',
                        help='Download audio only')
    parser.add_argument('-p', '--playlist', action='store_true',
                        help='Force playlist download')
    parser.add_argument('-s', '--single', action='store_true',
                        help='Download single video from playlist URL')
    parser.add_argument('-m', '--max-downloads', type=int,
                        help='Maximum number of videos to download from playlist')
    parser.add_argument('-l', '--list-formats', action='store_true',
                        help='List available formats without downloading')
    parser.add_argument('-i', '--info', action='store_true',
                        help='Show video information without downloading')

    args = parser.parse_args()

    # Create downloader instance
    downloader = YouTubeDownloader(args.output)

    # List formats if requested
    if args.list_formats:
        downloader.list_formats(args.url)
        return

    # Show info if requested
    if args.info:
        info = downloader.get_video_info(args.url)
        if info:
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Duration: {info.get('duration', 'N/A')} seconds")
            print(f"View count: {info.get('view_count', 'N/A')}")
            print(f"Upload date: {info.get('upload_date', 'N/A')}")
            print(f"Uploader: {info.get('uploader', 'N/A')}")
        return

    # Determine if it's a playlist
    is_playlist = downloader.is_playlist(args.url)

    if args.single and is_playlist:
        # Force single video download from playlist URL
        print("Downloading single video from playlist URL...")
        success = downloader.download_video(
            args.url, args.quality, args.audio_only)
    elif args.playlist or is_playlist:
        # Download playlist
        print("Downloading playlist...")
        success = downloader.download_playlist(
            args.url, args.quality, args.audio_only, args.max_downloads)
    else:
        # Download single video
        print("Downloading single video...")
        success = downloader.download_video(
            args.url, args.quality, args.audio_only)

    if success:
        print(f"Files saved to: {downloader.output_dir}")
    else:
        print("Download failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
