from fastapi.testclient import TestClient

import database.database as database_module
from main import app
from services.auth.google_auth_service import google_auth_service


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