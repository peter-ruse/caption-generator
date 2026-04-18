from datetime import UTC, datetime

from fastapi import APIRouter

health_router = APIRouter(tags=["health"])


@health_router.get("/healthz")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now(UTC)}
