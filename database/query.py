from datetime import UTC, datetime, timedelta
from typing import Any

import asyncpg


async def get_model_success_rate(
    db_conn: asyncpg.Connection, hours: int = 24
) -> dict[str, Any]:
    """Get success rate per model for the last N hours"""
    since = datetime.now(UTC) - timedelta(hours=hours)
    try:
        results = await db_conn.fetch(
            """
            SELECT 
                model,
                COUNT(*) as total,
                SUM(CASE WHEN success = true THEN 1 ELSE 0 END) as successes,
                ROUND(SUM(CASE WHEN success = true THEN 1 ELSE 0 END) * 100.0 / COUNT(*) :: NUMERIC, 2) as success_rate,
                ROUND(AVG(latency_ms) :: NUMERIC, 2) as avg_latency_ms
            FROM events
            WHERE timestamp > $1
            GROUP BY model
            ORDER BY success_rate DESC
            """,
            since,
        )

        return {
            "period_hours": hours,
            "models": [
                {
                    "model": row["model"],
                    "total_requests": row["total"],
                    "successes": row["successes"],
                    "success_rate": row["success_rate"],
                    "avg_latency_ms": row["avg_latency_ms"],
                }
                for row in results
            ],
        }
    except Exception as e:
        return {"error": str(e)}


async def get_platform_stats(
    db_conn: asyncpg.Connection, hours: int = 24
) -> dict[str, Any]:
    """Get stats per platform"""
    since = datetime.now(UTC) - timedelta(hours=hours)
    try:
        results = await db_conn.fetch(
            """
            SELECT 
                platform,
                COUNT(*) as total,
                SUM(CASE WHEN success = true THEN 1 ELSE 0 END) as successes,
                ROUND(SUM(CASE WHEN success = true THEN 1 ELSE 0 END) * 100.0 / COUNT(*) :: NUMERIC, 2) as success_rate,
                ROUND(AVG(tags_count) :: NUMERIC, 1) as avg_tags,
                ROUND(AVG(prompt_token_count) :: NUMERIC, 1) as avg_prompt_tokens,
                ROUND(AVG(output_token_count) :: NUMERIC, 1) as avg_output_tokens
            FROM events
            WHERE timestamp > $1
            GROUP BY platform
            ORDER BY total DESC
            """,
            since,
        )

        return {
            "period_hours": hours,
            "platforms": [
                {
                    "platform": row["platform"],
                    "total_requests": row["total"],
                    "successes": row["successes"],
                    "success_rate": row["success_rate"],
                    "avg_tags": row["avg_tags"],
                    "avg_prompt_tokens": row["avg_prompt_tokens"],
                    "avg_output_tokens": row["avg_output_tokens"],
                }
                for row in results
            ],
        }
    except Exception as e:
        return {"error": str(e)}


async def get_error_summary(
    db_conn: asyncpg.Connection, hours: int = 24
) -> dict[str, Any]:
    """Get summary of recent errors"""
    since = datetime.now(UTC) - timedelta(hours=hours)
    try:
        results = await db_conn.fetch(
            """
            SELECT 
                error_message,
                COUNT(*) as count
            FROM events
            WHERE success = false AND timestamp > $1 AND error_message IS NOT NULL
            GROUP BY error_message
            ORDER BY count DESC
            LIMIT 10
            """,
            since,
        )

        return {
            "period_hours": hours,
            "errors": [
                {"message": row["error_message"], "count": row["count"]}
                for row in results
            ],
        }
    except Exception as e:
        return {"error": str(e)}
