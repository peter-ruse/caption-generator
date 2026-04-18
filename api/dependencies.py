from fastapi import Cookie

from analytics.logger import AnalyticsLogger, analytics_logger
from api.exceptions import AuthRequiredException
from core.auth import decode_access_token


def get_current_user(access_token: str = Cookie(None)):
    # NOTE: FastAPI expects the arg name to exactly match the key
    # that we passed in to set_cookie in the auth_callback path operation
    if not access_token:
        raise AuthRequiredException()

    try:
        data = decode_access_token(access_token)

        if (username := data.get("sub")) is None:
            raise AuthRequiredException()

        return username
    except Exception:
        raise AuthRequiredException()


def get_analytics_logger() -> AnalyticsLogger:
    """Dependency for analytics logger"""
    return analytics_logger
