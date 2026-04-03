from typing import Annotated

from pydantic import AfterValidator, BaseModel, HttpUrl

from core.enums import CaptionStyle, SocialMediaPlatform
from services.enums import Provider


def http_url_to_str(url: HttpUrl) -> str:
    return url.encoded_string()


def str_to_caption_style(caption_style: str) -> CaptionStyle:
    return CaptionStyle[caption_style.upper()]


class GenerateCaptionRequest(BaseModel):
    link: Annotated[HttpUrl, AfterValidator(http_url_to_str)]
    title: str
    text: str
    social_media_platform: SocialMediaPlatform
    caption_style: Annotated[str, AfterValidator(str_to_caption_style)]
    custom_instruction: str = ""
    provider: Provider = Provider.GEMINI
