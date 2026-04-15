from api.schemas import GenerateCaptionRequest
from core.enums import CaptionStyle


def test_generate_caption_request_coerces_caption_style() -> None:
    request = GenerateCaptionRequest.model_validate(
        {
            "link": "https://example.com/post",
            "title": "Title",
            "text": "Body",
            "social_media_platform": "Instagram",
            "caption_style": "medium",
            "custom_instruction": "",
        }
    )

    assert request.caption_style == CaptionStyle.MEDIUM


def test_generate_caption_request_converts_link_to_string() -> None:
    request = GenerateCaptionRequest.model_validate(
        {
            "link": "https://example.com/post",
            "title": "Title",
            "text": "Body",
            "social_media_platform": "LinkedIn",
            "caption_style": "LONG",
            "custom_instruction": "Keep it concise",
        }
    )

    assert isinstance(request.link, str)
    assert request.link == "https://example.com/post"
