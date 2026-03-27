import logging
import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.routes import router
from core.enums import CaptionStyle, SocialMediaPlatform

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = FastAPI(
    title="Caption Generator", swagger_ui_parameters={"displayRequestDuration": True}
)
app.include_router(router)

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
