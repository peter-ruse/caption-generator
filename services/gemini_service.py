from google import genai

from core.enums import CaptionStyle, SocialMediaPlatform
from services.base import LLMService


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
        text: str,
        caption_style: CaptionStyle,
        social_media_platform: SocialMediaPlatform,
    ) -> str:
        prompt = f"Write {caption_style.value.prompt}, with emojis where appropriate, summarizing: {text}"

        system_instruction = (
            "Act as a professional social media strategist. "
            "Output only the caption text itself. "
            "Do not include introductions, explanations, multiple options, or conversational filler. "
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
            except Exception as e:
                continue

        return "All models exhausted. Please wait and try again."
