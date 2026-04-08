import logging
import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.generation import gen_router
from api.health import health_router
from config import app_settings
from core.enums import CaptionStyle, SocialMediaPlatform

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


app = FastAPI(**fastapi_settings)
app.include_router(gen_router)
app.include_router(health_router)
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
