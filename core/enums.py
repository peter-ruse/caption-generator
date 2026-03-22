from enum import Enum, StrEnum
from typing import NamedTuple


class StyleInfo(NamedTuple):
    prompt: str
    label: str  # useful for the UI


class CaptionStyle(Enum):
    SHORT = StyleInfo(prompt="1-2 sentences", label="Short")
    MEDIUM = StyleInfo(prompt="3-4 sentences", label="Medium")
    LONG = StyleInfo(prompt="5-6 sentences", label="Long")


class SocialMediaPlatform(StrEnum):
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    LINKEDIN = "LinkedIn"
