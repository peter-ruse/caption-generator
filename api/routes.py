from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from api.schemas import GenerateCaptionRequest
from services.factory import LLMServiceFactory
from services.prompt_manager import PromptManager

router = APIRouter(tags=["generation"])


@router.post("/generate_caption")
async def generate_caption(request: GenerateCaptionRequest):
    service = LLMServiceFactory.get_service_from_provider(request.provider)
    prompt = PromptManager.generate_prompt(
        request.title, request.text, request.caption_style  # type: ignore
    )
    system_instruction = PromptManager.generate_system_instruction(
        request.social_media_platform, request.custom_instruction
    )
    caption = service.generate_caption(prompt, system_instruction)

    if caption:
        return HTMLResponse(
            f"""
            <div id="caption-text" class="text-gray-800 leading-relaxed whitespace-pre-wrap fade-in">{caption}\n\nFor more details, please visit {request.link}</div>
            <button onclick="copyToClipboard()" id="copy-btn" 
                class="mt-6 w-full py-3 border border-black text-black font-bold rounded-xl hover:bg-gray-50 transition-all fade-in">
                Copy to Clipboard
            </button>
            """
        )
    else:
        return HTMLResponse(
            """
            <div id="caption-text" class="fade-in p-4 rounded-xl border border-rose-100 bg-rose-50/50">
                <div class="flex items-start gap-3">
                    <svg class="w-5 h-5 text-rose-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                        <h3 class="text-sm font-semibold text-rose-800 uppercase tracking-tight">Generation Error</h3>
                        <p class="text-sm text-rose-700 leading-relaxed mt-1">
                            Sorry, we couldn't generate a caption, probably due to an API issue. Please come back and try again later.
                        </p>
                    </div>
                </div>
            </div>
            """
        )
