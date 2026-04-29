import logging

import asyncpg

from analytics.models import AnalyticsRecord

logger = logging.getLogger(__name__)


class AnalyticsLogger:
    async def log_event(self, record: AnalyticsRecord, db_conn: asyncpg.Connection):
        """Log an analytics event to the database"""
        try:
            await db_conn.execute(
                """
                INSERT INTO events 
                (
                    timestamp, 
                    model, 
                    username, 
                    platform, 
                    caption_style, 
                    success, 
                    latency_ms, 
                    error_message, 
                    tags_count,
                    prompt_token_count,
                    output_token_count
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """,
                record.timestamp,
                record.model,
                record.username,
                record.platform,
                record.caption_style,
                record.success,
                record.latency_ms,
                record.error_message,
                record.tags_count,
                record.prompt_token_count,
                record.output_token_count,
            )
        except Exception as error:
            logger.error("Failed to log analytics event: %s", error)


analytics_logger = AnalyticsLogger()
