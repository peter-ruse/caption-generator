import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.analytics import analytics_router
from api.generation import gen_router
from api.health import health_router
from config import app_settings
from core.enums import CaptionStyle, SocialMediaPlatform
from database.database import Database, init_db

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
    yield
    await db.disconnect()


app = FastAPI(**fastapi_settings, lifespan=lifespan)
app.include_router(gen_router)
app.include_router(health_router)
app.include_router(analytics_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "CaptionStyle": CaptionStyle,
            "SocialMediaPlatform": SocialMediaPlatform,
        },
    )
