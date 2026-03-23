from core.enums import CaptionStyle, SocialMediaPlatform


class PromptManager:
    @classmethod
    def generate_prompt(cls, title: str, text: str, caption_style: CaptionStyle) -> str:
        return (
            f"Write {caption_style.value.length_in_sentences} sentences, with emojis where appropriate, "
            f"summarizing the article '{title}': {text}"
        )

    @classmethod
    def generate_system_instruction(
        cls,
        social_media_platform: SocialMediaPlatform,
        custom_instruction: str | None,
    ) -> str:
        base_instruction = (
            "Act as a professional social media strategist catering mostly to Australian tourists in Bali.\n"
            "Output only the requested content followed by a small cluster of 3-5 relevant and trending hashtags.\n"
            "Do NOT include introductions, explanations, multiple options, or conversational filler.\n"
            "Adhere strictly to the specified number of sentences.\n"
            f"Adhere to {social_media_platform}'s specific character limits and cultural tone."
        )

        if custom_instruction:
            return (
                f"{base_instruction}\n\nAdditional instruction:\n{custom_instruction}"
            )
        else:
            return base_instruction
