import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, cast

import asyncpg

from core.config import postgresql_settings
from utils.meta import SingletonMeta

logger = logging.getLogger(__name__)


class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> asyncpg.Pool:
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(
                    user=postgresql_settings.user,
                    password=postgresql_settings.raw_password,
                    host=postgresql_settings.host,
                    port=postgresql_settings.port,
                    database=postgresql_settings.database,
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


@asynccontextmanager
async def acquire_db_conn() -> AsyncGenerator[asyncpg.Connection, None]:
    pool = await Database().connect()
    async with pool.acquire() as conn:
        yield cast(asyncpg.Connection, conn)


async def get_db_conn() -> AsyncGenerator[asyncpg.Connection, None]:
    async with acquire_db_conn() as conn:
        yield conn


async def init_db():
    """Initialize database schema and tables"""
    try:
        async with acquire_db_conn() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ NOT NULL,
                    username TEXT,
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
    except Exception as error:
        logger.error(
            "Database initialization failed. App will continue without DB features: %s",
            error,
        )


async def close_db():
    await Database().disconnect()


@asynccontextmanager
async def db_lifecycle():
    await init_db()
    yield
    await close_db()
