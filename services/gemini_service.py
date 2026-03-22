import logging
import sys

from google import genai
from google.genai import errors

from core.enums import CaptionStyle, SocialMediaPlatform
from services.base import LLMService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class GeminiService(LLMService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.models = [
            "gemini-3.1-flash-lite-preview",
            "gemini-3-flash-preview",
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
        ]

    def generate_caption(
        self,
        title: str,
        text: str,
        caption_style: CaptionStyle,
        social_media_platform: SocialMediaPlatform,
    ) -> str | None:
        prompt = (
            f"Write {caption_style.value.length_in_sentences} sentences, with emojis where appropriate, "
            f"summarizing the article '{title}': {text}"
        )

        system_instruction = (
            "Act as a professional social media strategist. "
            "Output only the caption text followed by a small cluster of 3-5 relevant and trending hashtags. "
            "Do NOT include introductions, explanations, multiple options, or conversational filler. "
            "Do NOT exceed the specified number of sentences."
            f"Adhere to {social_media_platform}'s specific character limits and cultural tone."
        )

        for model in self.models:
            try:
                content = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={
                        "system_instruction": system_instruction,
                        "temperature": 0.7,
                    },
                )
                return content.text or ""
            except errors.ClientError as e:
                logger.error(f"Client error: {e}")
            except errors.ServerError as e:
                logger.error(f"Server error: {e}")
            except errors.APIError as e:
                logger.error(f"General API error: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
