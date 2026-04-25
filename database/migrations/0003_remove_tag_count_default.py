from yoyo import step

step(
    """
    ALTER TABLE events ALTER COLUMN tags_count DROP DEFAULT;
    """
)
