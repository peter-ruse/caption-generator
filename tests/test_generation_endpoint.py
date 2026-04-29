import asyncio

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.dependencies import get_analytics_logger, rate_limit_check
from api.routes.generation import gen_router
from database.database import get_db_conn
from services.llm.models import CaptionGenerationResult


class DummyLogger:
    async def log_event(self, record, db_conn):
        await asyncio.sleep(0.01)


class DummyServiceSuccess:
    async def generate_caption(self, prompt: str, system_instruction: str):
        await asyncio.sleep(0.01)
        return CaptionGenerationResult(
            model="dummy-model",
            latency_ms=100,
            caption="A sample caption.",
            tags=["#bali", "#travel"],
            prompt_token_count=3,
            output_token_count=3,
        )


class DummyServiceFailure:
    async def generate_caption(self, prompt: str, system_instruction: str):
        await asyncio.sleep(0.01)


async def _fake_db_conn():
    yield object()


def _make_client() -> TestClient:
    app = FastAPI()
    app.include_router(gen_router)
    app.dependency_overrides[get_analytics_logger] = lambda: DummyLogger()
    app.dependency_overrides[rate_limit_check] = lambda: "test-user"
    app.dependency_overrides[get_db_conn] = _fake_db_conn
    return TestClient(app)


def test_generate_caption_success_renders_caption_and_tags(monkeypatch):
    from services.llm.factory import LLMServiceFactory

    monkeypatch.setattr(
        LLMServiceFactory,
        "get_service_from_provider",
        classmethod(lambda cls, provider: DummyServiceSuccess()),
    )

    client = _make_client()
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
    assert "A sample caption." in response.text
    assert "#bali" in response.text
    assert "Copy to Clipboard" in response.text


def test_generate_caption_failure_renders_error(monkeypatch):
    from services.llm.factory import LLMServiceFactory

    monkeypatch.setattr(
        LLMServiceFactory,
        "get_service_from_provider",
        classmethod(lambda cls, provider: DummyServiceFailure()),
    )

    client = _make_client()
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
    assert "Generation Error" in response.text
    assert "couldn't generate a caption" in response.text


def test_generate_caption_succeeds_when_background_db_logging_fails(monkeypatch):
    from services.llm.factory import LLMServiceFactory

    class FailingAcquireDbConn:
        async def __aenter__(self):
            raise RuntimeError("database unavailable")

        async def __aexit__(self, exc_type, exc, tb):
            return False

    def failing_acquire_db_conn():
        return FailingAcquireDbConn()

    monkeypatch.setattr(
        LLMServiceFactory,
        "get_service_from_provider",
        classmethod(lambda cls, provider: DummyServiceSuccess()),
    )

    import api.routes.generation as generation_module

    monkeypatch.setattr(
        generation_module,
        "acquire_db_conn",
        failing_acquire_db_conn,
    )

    client = _make_client()
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
    assert "A sample caption." in response.text
    assert "#bali" in response.text
