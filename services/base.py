from typing import Protocol


class LLMService(Protocol):
    model: str | None
    latency_ms: int | None

    async def generate_caption(
        self, prompt: str, system_instruction: str
    ) -> tuple[str, list[str]] | None: ...
