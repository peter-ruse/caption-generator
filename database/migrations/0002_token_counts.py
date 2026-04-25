from yoyo import step

step(
    """
    ALTER TABLE events ADD COLUMN IF NOT EXISTS prompt_token_count INTEGER;
    ALTER TABLE events ADD COLUMN IF NOT EXISTS output_token_count INTEGER;
    """,
    """
    ALTER TABLE events DROP COLUMN prompt_token_count INTEGER;
    ALTER TABLE events DROP COLUMN output_token_count INTEGER;
    """,
)
