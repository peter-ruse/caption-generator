import logging
import time

from services.redis_service import RedisService
from utils.meta import SingletonMeta

logger = logging.getLogger(__name__)


class RateLimitingService(metaclass=SingletonMeta):
    def __init__(self, prefix="rate-limit"):
        self.redis_service = RedisService()
        self.prefix = prefix

    @property
    def client(self):
        return self.redis_service.client

    def _make_full_key(self, key: str):
        return f"{self.prefix}:{key}"

    async def is_rate_limited(self, key: str, limit: int, window: int) -> bool:
        full_key = self._make_full_key(key)
        pipeline = self.client.pipeline(transaction=True)
        now = time.time()
        window_start = now - window

        try:
            pipeline.zremrangebyscore(full_key, 0, window_start)
            pipeline.zadd(full_key, {str(now): now})
            pipeline.zcard(full_key)
            pipeline.expire(full_key, window + 1)

            _, _, current_count, _ = await pipeline.execute()

            return current_count > limit
        except Exception as e:
            logger.error(f"Rate limiter error: {e}")
            return False
