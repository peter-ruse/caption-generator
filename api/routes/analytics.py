from typing import Annotated

import asyncpg
from fastapi import APIRouter, Depends

from database.database import get_db_conn
from database.query import get_error_summary, get_model_success_rate, get_platform_stats

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])


@analytics_router.get("/models")
async def get_models_analytics(
    db_conn: Annotated[asyncpg.Connection, Depends(get_db_conn)], hours: int = 24
):
    """Get success rate and performance metrics per model"""
    return await get_model_success_rate(db_conn, hours=hours)


@analytics_router.get("/platforms")
async def get_platforms_analytics(
    db_conn: Annotated[asyncpg.Connection, Depends(get_db_conn)], hours: int = 24
):
    """Get usage and success stats per platform"""
    return await get_platform_stats(db_conn, hours=hours)


@analytics_router.get("/errors")
async def get_errors_analytics(
    db_conn: Annotated[asyncpg.Connection, Depends(get_db_conn)], hours: int = 24
):
    """Get summary of recent errors"""
    return await get_error_summary(db_conn, hours=hours)
