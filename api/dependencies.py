from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status

from analytics.logger import AnalyticsLogger, analytics_logger
from api.exceptions import AdminRequiredException, AuthRequiredException
from core.auth import decode_access_token
from core.config import app_settings, redis_settings
from services.rate_limiting.rate_limiting_service import RateLimitingService


def get_current_session(access_token: str = Cookie(None)) -> dict:
    # NOTE: FastAPI expects the arg name to exactly match the key
    # that we passed in to set_cookie in the auth_callback path operation
    if not access_token:
        raise AuthRequiredException()

    try:
        session = decode_access_token(access_token)

        if session.get("sub") is None:
            raise AuthRequiredException()

        return session
    except Exception:
        raise AuthRequiredException()


def get_analytics_logger() -> AnalyticsLogger:
    """Dependency for analytics logger"""
    return analytics_logger


def require_admin(
    session: Annotated[dict, Depends(get_current_session)],
) -> None:
    """Dependency for ensuring the current user is the admin. Raises AdminRequiredException otherwise."""
    if session["sub"] != app_settings.admin_username:
        raise AdminRequiredException()


async def rate_limit_check(session: Annotated[dict, Depends(get_current_session)]):
    username = session["sub"]
    if await RateLimitingService().is_rate_limited(
        key=username,
        limit=redis_settings.rate_limit,
        window=redis_settings.rate_limit_window_seconds,
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests"
        )
    return username
