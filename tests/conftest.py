import os

# Ensure all required settings are present during test imports.
os.environ.setdefault("ENV", "test")
os.environ.setdefault("ADMIN_USERNAME", "test-admin@example.com")
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-google-client-id")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "test-google-client-secret")
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-api-key")
os.environ.setdefault("POSTGRES_USER", "test-postgres-user")
os.environ.setdefault("POSTGRES_PASSWORD", "test-postgres-password")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_DATABASE", "test-postgres-db")
os.environ.setdefault("SECRET_KEY", "test-jwt-secret")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("RATE_LIMIT", "5")
os.environ.setdefault("RATE_LIMIT_WINDOW_SECONDS", "60")
