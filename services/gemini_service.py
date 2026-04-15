import logging
import time

from google import genai
from google.genai import errors

from config import gemini_settings
from services.base import LLMService

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
        self.model: str | None = None
        self.latency_ms: float | None = None

    async def generate_caption(
        self, prompt: str, system_instruction: str
    ) -> tuple[str, list[str]] | None:
        for model in self.models:
            self.model = model
            self.latency_ms = None
            try:
                start = time.perf_counter()
                response = await self.client.aio.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={
                        "system_instruction": system_instruction,
                        "temperature": 0.7,
                    },
                )
                self.latency_ms = (time.perf_counter() - start) * 1000.0
                content = response.text or ""

                if "TAGS:" in content:
                    caption, tags = content.split("TAGS:")
                    caption = caption.strip()
                    tags = tags.strip().split()
                    return caption, tags
                return content, ["Bali", "BaliLife", "TravelBali", "VisitBali"]
            except errors.ClientError as e:
                logger.error(f"Client error: {e}")
            except errors.ServerError as e:
                logger.error(f"Server error: {e}")
            except errors.APIError as e:
                logger.error(f"General API error: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error: {e}")


gemini_service = GeminiService(gemini_settings.raw_api_key)
