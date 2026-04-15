import asyncio

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.dependencies import get_analytics_logger
from api.generation import gen_router
from database.database import get_db_conn


class DummyLogger:
    async def log_event(self, record, db_conn):
        await asyncio.sleep(0.01)


class DummyServiceSuccess:
    model = "dummy-model"
    latency_ms = 100

    async def generate_caption(self, prompt: str, system_instruction: str):
        await asyncio.sleep(0.01)
        return ("A sample caption.", ["#bali", "#travel"])


class DummyServiceFailure:
    model = None
    latency_ms = None

    async def generate_caption(self, prompt: str, system_instruction: str):
        await asyncio.sleep(0.01)


async def _fake_db_conn():
    yield object()


def _make_client() -> TestClient:
    app = FastAPI()
    app.include_router(gen_router)
    app.dependency_overrides[get_analytics_logger] = lambda: DummyLogger()
    app.dependency_overrides[get_db_conn] = _fake_db_conn
    return TestClient(app)


def test_generate_caption_success_renders_caption_and_tags(monkeypatch):
    from services.factory import LLMServiceFactory

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
    from services.factory import LLMServiceFactory

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
