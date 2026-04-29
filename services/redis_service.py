from redis.asyncio import Redis

from core.config import redis_settings
from utils.meta import SingletonMeta


class RedisService(metaclass=SingletonMeta):
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = Redis.from_url(redis_settings.raw_url)
        return self._client
