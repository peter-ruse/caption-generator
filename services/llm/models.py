from pydantic import BaseModel


class CaptionGenerationResult(BaseModel):
    model: str
    latency_ms: int
    caption: str
    tags: list[str]
    prompt_token_count: int | None
    output_token_count: int | None
