import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, cast
from urllib.parse import quote_plus

import asyncpg
from yoyo import get_backend, read_migrations
from yoyo.backends import PostgresqlBackend

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


def init_db():
    """Initialize database schema and tables"""
    try:
        user = postgresql_settings.user
        password = quote_plus(postgresql_settings.raw_password)
        host = postgresql_settings.host
        port = postgresql_settings.port
        database = postgresql_settings.database
        backend: PostgresqlBackend = get_backend(
            f"postgresql://{user}:{password}@{host}:{port}/{database}"
        )
        migrations = read_migrations(str(Path(__file__).parents[0] / "migrations"))
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
    except Exception as error:
        logger.error(
            "Database initialization failed. App will continue without DB features: %s",
            error,
        )


async def close_db():
    await Database().disconnect()


@asynccontextmanager
async def db_lifecycle():
    init_db()
    yield
    await close_db()
