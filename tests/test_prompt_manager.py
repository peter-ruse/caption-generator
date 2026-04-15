from core.enums import CaptionStyle, SocialMediaPlatform
from services.prompt_manager import PromptManager


def test_build_prompt_includes_custom_instruction_when_provided() -> None:
    prompt = PromptManager.build_prompt(
        title="A Great Day",
        text="Some source text",
        link="https://example.com/article",
        caption_style=CaptionStyle.SHORT,
        custom_instruction="Use an upbeat tone.",
    )

    assert "Title: A Great Day" in prompt
    assert "approximately 1-2 sentences" in prompt
    assert "Use an upbeat tone." in prompt


def test_build_prompt_omits_custom_instruction_when_blank() -> None:
    prompt = PromptManager.build_prompt(
        title="A Great Day",
        text="Some source text",
        link="https://example.com/article",
        caption_style=CaptionStyle.MEDIUM,
        custom_instruction="   ",
    )

    assert "Title: A Great Day" in prompt
    assert "approximately 2-3 sentences" in prompt
    assert "Use an upbeat tone." not in prompt


def test_build_system_instruction_mentions_platform() -> None:
    instruction = PromptManager.build_system_instruction(
        SocialMediaPlatform.INSTAGRAM
    )

    assert "Instagram" in instruction
    assert "TAGS:" in instruction
