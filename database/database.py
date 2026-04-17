import logging

import asyncpg

from config import postgresql_settings
from utils.meta import SingletonMeta

logger = logging.getLogger(__name__)


class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> asyncpg.Pool:
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(
                    dsn=postgresql_settings.raw_url,
                    min_size=5,
                    max_size=20,
                    command_timeout=60,
                )
                logger.info("PostgreSQL connection pool established.")
            except Exception as e:
                logger.critical(f"Couldn't connect to PostgreSQL: {e}")
                raise e
        return self.pool

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
            logger.info("PostgreSQL connection pool closed.")


async def get_db_conn():
    pool = await Database().connect()

    async with pool.acquire() as conn:
        yield conn


async def init_db():
    """Initialize database schema and tables"""
    db = Database()
    pool = await db.connect()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                model TEXT,
                platform TEXT NOT NULL,
                caption_style TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                latency_ms INTEGER NOT NULL,
                error_message TEXT,
                tags_count INTEGER DEFAULT 0
            )
            """
        )

    logger.info("Database initialization complete.")
