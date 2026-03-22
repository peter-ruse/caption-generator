from typing import Protocol

from core.enums import CaptionStyle, SocialMediaPlatform


class LLMService(Protocol):
    def generate_caption(
        self,
        title: str,
        text: str,
        caption_style: CaptionStyle,
        social_media_platform: SocialMediaPlatform,
    ) -> str: ...
