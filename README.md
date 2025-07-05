# YouTube Downloader

A simple Python script to download YouTube videos and playlists using yt-dlp.

## Features

- Download single videos or entire playlists
- Choose video quality (best, worst, or specific resolution)
- Audio-only downloads
- Video information display
- Format listing
- Customizable output directory

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Examples

```bash
# Download a video
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Download audio only
python main.py -a "https://www.youtube.com/watch?v=VIDEO_ID"

# Download with specific quality
python main.py -q 720 "https://www.youtube.com/watch?v=VIDEO_ID"

# Download playlist
python main.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# Download first 5 videos from playlist
python main.py -m 5 "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Command Options

- `-o, --output`: Output directory (default: downloads)
- `-q, --quality`: Video quality - best, worst, or height (e.g., 720, 1080)
- `-a, --audio-only`: Download audio only
- `-p, --playlist`: Force playlist download
- `-s, --single`: Download single video from playlist URL
- `-m, --max-downloads`: Maximum number of videos from playlist
- `-l, --list-formats`: List available formats
- `-i, --info`: Show video information

## Requirements

- Python 3.6+
- yt-dlp

## License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws.
