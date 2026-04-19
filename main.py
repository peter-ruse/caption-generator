import logging
import sys
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.dependencies import get_current_session
from api.exceptions import AuthRequiredException
from api.routes.analytics import analytics_router
from api.routes.auth import auth_router
from api.routes.generation import gen_router
from api.routes.health import health_router
from core.config import app_settings
from core.enums import CaptionStyle, SocialMediaPlatform
from database.database import Database, init_db
from services.auth.google_auth_service import google_auth_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

fastapi_settings = {
    "title": "Caption Generator",
    "swagger_ui_parameters": {"displayRequestDuration": True},
}
if app_settings.env == "prod":
    fastapi_settings.update({"docs_url": None, "redoc_url": None, "openapi_url": None})


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database()
    await db.connect()
    await init_db()
    google_auth_service.init_httpx_client()
    yield
    await google_auth_service.close_httpx_client()
    await db.disconnect()


app = FastAPI(**fastapi_settings, lifespan=lifespan)
app.include_router(auth_router)
app.include_router(gen_router)
app.include_router(health_router)
app.include_router(analytics_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.exception_handler(AuthRequiredException)
async def auth_exception_handler(request: Request, exc: AuthRequiredException):
    if "HX-Request" in request.headers:
        return JSONResponse(status_code=401, content={"detail": "Token expired"})

    return RedirectResponse(url="/login", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    session: Annotated[dict, Depends(get_current_session)],
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "CaptionStyle": CaptionStyle,
            "SocialMediaPlatform": SocialMediaPlatform,
            "username": session["sub"],
            "session_expiry": session["exp"],
        },
    )
