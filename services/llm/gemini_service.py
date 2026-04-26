import logging
import time
from typing import cast

from google import genai
from google.genai import errors

from core.config import gemini_settings
from services.llm.base import LLMService
from services.llm.models import CaptionGenerationResult

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

    async def generate_caption(
        self, prompt: str, system_instruction: str
    ) -> CaptionGenerationResult | None:
        for model in self.models:
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

                usage_metadata = response.usage_metadata
                prompt_token_count, output_token_count = (
                    (None, None)
                    if usage_metadata is None
                    else (
                        usage_metadata.prompt_token_count,
                        usage_metadata.candidates_token_count,
                    )
                )

                latency_ms = round((time.perf_counter() - start) * 1000)
                content = response.text or ""

                if "TAGS:" in content:
                    caption, tags = content.split("TAGS:")
                    caption = caption.strip()
                    tags = tags.strip().split()
                else:
                    caption = content
                    tags = ["Bali", "BaliLife", "TravelBali", "VisitBali"]
                return CaptionGenerationResult(
                    model=model,
                    latency_ms=latency_ms,
                    caption=caption,
                    tags=tags,
                    prompt_token_count=prompt_token_count,
                    output_token_count=output_token_count,
                )
            except errors.ClientError as e:
                logger.error(f"Client error: {e}")
            except errors.ServerError as e:
                logger.error(f"Server error: {e}")
            except errors.APIError as e:
                logger.error(f"General API error: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error: {e}")


gemini_service = GeminiService(gemini_settings.raw_api_key)
