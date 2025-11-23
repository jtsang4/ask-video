import logging
from typing import Optional
import yt_dlp

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def download_subtitles(url: str) -> Optional[str]:
    """
    Downloads subtitles for a given video URL using yt-dlp.
    Returns the subtitle content as a string, or None if no subtitles are found.
    """
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en", "zh-Hans", "zh-Hant", "zh"],
        "subtitlesformat": "vtt",
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Check for manually created subtitles first
            subtitles = info.get("subtitles", {})
            auto_subtitles = info.get("automatic_captions", {})

            # Prioritize Chinese and English
            langs = ["zh-Hans", "zh-Hant", "zh", "en"]

            selected_sub = None

            # Try manual subtitles
            for lang in langs:
                if lang in subtitles:
                    selected_sub = subtitles[lang]
                    break

            # If no manual, try auto subtitles
            if not selected_sub:
                for lang in langs:
                    if lang in auto_subtitles:
                        selected_sub = auto_subtitles[lang]
                        break

            # Fallback to any available subtitle if preferred langs not found
            if not selected_sub:
                if subtitles:
                    selected_sub = list(subtitles.values())[0]
                elif auto_subtitles:
                    selected_sub = list(auto_subtitles.values())[0]

            if not selected_sub:
                logger.warning("No subtitles found for this video.")
                return None

            # Download the subtitle content
            # Since we set skip_download=True, extract_info won't download the video.
            # But we need to download the subtitle file.
            # yt-dlp doesn't have a direct "download subtitle to string" method easily exposed without downloading file.
            # So we will use a different approach: let yt-dlp download the sub file to a temp path or memory.

            # Actually, the 'url' in the subtitle dict points to the subtitle file.
            # We can fetch it.

            # Let's find the vtt or srv3 format
            sub_url = None
            for fmt in selected_sub:
                if fmt.get("ext") in ["vtt", "srv3", "json3"]:
                    sub_url = fmt["url"]
                    break

            if not sub_url:
                # Fallback to first available
                sub_url = selected_sub[0]["url"]

            import requests

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(sub_url, headers=headers)
            response.raise_for_status()

            return response.text

    except Exception as e:
        logger.error(f"Error processing video: {e}")
        return None
