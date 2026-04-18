from datetime import UTC, datetime, timedelta

from jose import jwt

from core.config import jwt_settings

ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data | {"exp": datetime.now(UTC) + timedelta(hours=24)}
    encoded_jwt = jwt.encode(
        to_encode, key=jwt_settings.raw_secret_key, algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str):
    return jwt.decode(token, key=jwt_settings.raw_secret_key, algorithms=[ALGORITHM])
