from enum import Enum, StrEnum
from typing import NamedTuple


class StyleInfo(NamedTuple):
    length_in_sentences: str
    label: str  # useful for the UI


class CaptionStyle(Enum):
    SHORT = StyleInfo(length_in_sentences="1-2", label="Short")
    MEDIUM = StyleInfo(length_in_sentences="2-3", label="Medium")
    LONG = StyleInfo(length_in_sentences="3-4", label="Long")


class SocialMediaPlatform(StrEnum):
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    LINKEDIN = "LinkedIn"
