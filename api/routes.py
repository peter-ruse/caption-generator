from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from api.schemas import GenerateCaptionRequest
from services.factory import LLMServiceFactory
from services.prompt_manager import PromptManager

router = APIRouter(tags=["generation"])


@router.post("/generate_caption")
async def generate_caption(request: GenerateCaptionRequest):
    service = LLMServiceFactory.get_service_from_provider(request.provider)
    prompt = PromptManager.build_prompt(
        request.title, request.text, request.link, request.caption_style, request.custom_instruction  # type: ignore
    )
    system_instruction = PromptManager.build_system_instruction(
        request.social_media_platform
    )
    result = await service.generate_caption(prompt, system_instruction)

    if result:
        caption, tags = result

        tag_buttons = "".join(
            [
                f'<button onclick="toggleTag(this)" data-tag="{t}" class="tag-btn px-3 py-1.5 border border-zinc-200 dark:border-zinc-700 rounded-full text-[11px] font-bold transition-all">{t}</button>'
                for t in tags
            ]
        )

        return HTMLResponse(
            f"""
            <div class="space-y-6 fade-in" id="container">
                <div id="base-template" style="display: none;">{caption}</div>

                <div id="caption-text" class="text-zinc-800 dark:text-zinc-100 leading-relaxed whitespace-pre-wrap">{caption}</div>

                <div class="space-y-3">
                    <p class="text-[10px] font-bold uppercase tracking-widest text-zinc-400">Suggested Hashtags</p>
                    <div class="flex flex-wrap gap-2">{tag_buttons}</div>
                </div>

                <button onclick="copyToClipboard()" id="copy-btn" 
                    class="mt-6 w-full py-3 border border-black dark:border-zinc-500 text-black dark:text-zinc-100 font-bold rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-all fade-in uppercase tracking-tight text-sm">
                    Copy to Clipboard
                </button>
            </div>
            """
        )
    else:
        return HTMLResponse(
            """
            <div id="caption-text" class="fade-in p-4 rounded-xl border border-rose-100 dark:border-rose-900/30 bg-rose-50/50 dark:bg-rose-950/20">
                <div class="flex items-start gap-3">
                    <svg class="w-5 h-5 text-rose-500 dark:text-rose-400 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    
                    <div>
                        <h3 class="text-sm font-semibold text-rose-800 dark:text-rose-200 uppercase tracking-tight">
                            Generation Error
                        </h3>
                        <p class="text-sm text-rose-700 dark:text-rose-300/90 leading-relaxed mt-1">
                            Sorry, we couldn't generate a caption, probably due to an API issue. Please come back and try again later.
                        </p>
                    </div>
                </div>
            </div>
            """
        )
