from typing import Protocol

from services.llm.models import CaptionGenerationResult


class LLMService(Protocol):
    async def generate_caption(
        self, prompt: str, system_instruction: str
    ) -> CaptionGenerationResult | None: ...
