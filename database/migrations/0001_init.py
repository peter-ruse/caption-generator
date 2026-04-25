from yoyo import step

step(
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
    """,
    """
    DROP TABLE events;
    """,
)
