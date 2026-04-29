import asyncio

from fastapi.testclient import TestClient

import database.database as database_module
from main import app
from services.auth.google_auth_service import google_auth_service
from services.llm.models import CaptionGenerationResult


def test_app_startup_succeeds_when_db_init_fails(monkeypatch):
    class FailingAcquireDbConn:
        async def __aenter__(self):
            raise RuntimeError("database unavailable")

        async def __aexit__(self, exc_type, exc, tb):
            return False

    def failing_acquire_db_conn():
        return FailingAcquireDbConn()

    monkeypatch.setattr(
        database_module,
        "acquire_db_conn",
        failing_acquire_db_conn,
    )

    with TestClient(app) as client:
        response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_google_auth_client_is_initialized_and_closed_by_lifespan():
    assert google_auth_service.httpx_client is None

    with TestClient(app):
        assert google_auth_service.httpx_client is not None

    assert google_auth_service.httpx_client is None


def test_generation_succeeds_even_when_db_startup_fails(monkeypatch):
    """Verify that app starts in degraded mode and generation still works when DB connection fails at startup."""

    async def failing_connect(self):
        raise RuntimeError("Database unavailable at startup")

    monkeypatch.setattr(
        database_module.Database,
        "connect",
        failing_connect,
    )

    from services.llm.factory import LLMServiceFactory

    class DummyLLMService:
        async def generate_caption(self, prompt: str, system_instruction: str):
            await asyncio.sleep(0.01)
            return CaptionGenerationResult(
                model="dummy-model",
                latency_ms=100,
                caption="A test caption.",
                tags=["#test"],
                prompt_token_count=3,
                output_token_count=3,
            )

    monkeypatch.setattr(
        LLMServiceFactory,
        "get_service_from_provider",
        classmethod(lambda cls, provider: DummyLLMService()),
    )

    class FailingDbConn:
        async def __aenter__(self):
            raise RuntimeError("Database unavailable")

        async def __aexit__(self, exc_type, exc, tb):
            return False

    def failing_acquire_db_conn():
        return FailingDbConn()

    import api.routes.generation as generation_module
    from api.dependencies import get_analytics_logger, rate_limit_check

    monkeypatch.setattr(
        generation_module,
        "acquire_db_conn",
        failing_acquire_db_conn,
    )

    def override_rate_limit_check():
        return "test-user"

    class DummyAnalyticsLogger:
        async def log_event(self, record, db_conn): ...

    app.dependency_overrides[rate_limit_check] = override_rate_limit_check
    app.dependency_overrides[get_analytics_logger] = lambda: DummyAnalyticsLogger()

    try:
        with TestClient(app) as client:
            response = client.get("/healthz")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"

            response = client.post(
                "/generate_caption",
                json={
                    "link": "https://example.com/post",
                    "title": "A title",
                    "text": "Some body text",
                    "social_media_platform": "Instagram",
                    "caption_style": "MEDIUM",
                    "custom_instruction": "",
                    "provider": "gemini",
                },
            )

            assert response.status_code == 200
            assert "A test caption." in response.text
            assert "#test" in response.text
    finally:
        app.dependency_overrides.clear()
