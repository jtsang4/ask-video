from abc import ABC, abstractmethod


class SubtitleFormatter(ABC):
    """
    Abstract base class for subtitle formatters.
    """

    @abstractmethod
    def format(self, content: str) -> str:
        """
        Formats the raw subtitle content into a readable string.
        """
        pass
