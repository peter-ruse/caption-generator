from typing import Annotated

from fastapi import Cookie, Depends

from analytics.logger import AnalyticsLogger, analytics_logger
from api.exceptions import AdminRequiredException, AuthRequiredException
from core.auth import decode_access_token
from core.config import app_settings


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
