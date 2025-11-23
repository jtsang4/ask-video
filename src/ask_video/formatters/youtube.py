import json
import logging
from .base import SubtitleFormatter

logger = logging.getLogger(__name__)


class YouTubeFormatter(SubtitleFormatter):
    """
    Formatter for YouTube subtitles (JSON3 format).
    """

    def format(self, content: str) -> str:
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            logger.warning(
                "Failed to parse subtitle content as JSON. Returning raw content."
            )
            return content

        if "events" not in data:
            # Not the expected JSON3 format, might be VTT or something else already
            return content

        formatted_lines = []
        for event in data["events"]:
            # Start time in milliseconds
            t_start_ms = event.get("tStartMs", 0)

            # Convert to MM:SS format
            seconds = t_start_ms // 1000
            minutes = seconds // 60
            seconds = seconds % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}]"

            # Get text segments
            segs = event.get("segs", [])
            text_parts = []
            for seg in segs:
                utf8 = seg.get("utf8", "")
                if utf8 and utf8 != "\n":
                    text_parts.append(utf8)

            text = "".join(text_parts).strip()

            if text:
                formatted_lines.append(f"{timestamp} {text}")

        return "\n".join(formatted_lines)
