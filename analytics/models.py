from datetime import UTC, datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field


def ensure_utc(timestamp: datetime) -> datetime:
    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=UTC)
    elif timestamp.tzinfo != UTC:
        raise ValueError("Timestamp must be in UTC")
    return timestamp


class AnalyticsRecord(BaseModel):
    username: str
    platform: str
    caption_style: str
    timestamp: Annotated[datetime, AfterValidator(ensure_utc)]
    success: bool
    model: str | None
    latency_ms: int | None
    error_message: str | None = None
    tags_count: int = Field(default=0)
