from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from api.schemas import GenerateCaptionRequest
from core.enums import SocialMediaPlatform
from services.factory import LLMServiceFactory

router = APIRouter(tags=["generation"])


@router.post("/generate_caption")
async def generate_caption(request: GenerateCaptionRequest):
    service = LLMServiceFactory.get_service_from_provider(request.provider)
    caption = service.generate_caption(
        request.title, request.text, request.caption_style, request.social_media_platform  # type: ignore
    )
    caption_with_link = f"{caption}\n\nFor more details, please visit {request.link}"

    return HTMLResponse(
        f"""
        <div id="caption-text" class="text-gray-800 leading-relaxed whitespace-pre-wrap fade-in">{caption_with_link}</div>
        <button onclick="copyToClipboard()" id="copy-btn" 
            class="mt-6 w-full py-3 border border-black text-black font-bold rounded-xl hover:bg-gray-50 transition-all fade-in">
            Copy to Clipboard
        </button>
        """
    )
