from typing import Protocol


class LLMService(Protocol):
    last_used_model: str

    async def generate_caption(
        self, prompt: str, system_instruction: str
    ) -> tuple[str, list[str]] | None: ...
