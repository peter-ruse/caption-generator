from typing import Protocol


class LLMService(Protocol):
    def generate_caption(self, prompt: str, system_instruction: str) -> str | None: ...
