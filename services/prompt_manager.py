from core.enums import CaptionStyle, SocialMediaPlatform


class PromptManager:
    @classmethod
    def build_prompt(cls, title: str, text: str, caption_style: CaptionStyle) -> str:
        return f"Write {caption_style.value.length_in_sentences} sentences summarizing the article '{title}': {text}"

    @classmethod
    def build_system_instruction(
        cls,
        social_media_platform: SocialMediaPlatform,
        custom_instruction: str,
    ) -> str:
        base_instruction = (
            "Act as a professional social media strategist catering mostly to Australian tourists in Bali.\n"
            "Don't make any references to Australia or Australians unless specifically asked to.\n"
            "Output only the requested content followed by a small cluster of 3-5 relevant and trending hashtags.\n"
            "Do NOT include introductions, explanations, multiple options, or conversational filler.\n"
            "Adhere strictly to the specified number of sentences, sometimes stated as a range; "
            "e.g., '1-2 sentences' means at least one but not more than two sentences.\n"
            "Be expressive and lively without being verbose; feel free to use emojis where appropriate."
            f"Adhere to {social_media_platform}'s specific character limits and cultural tone."
        )

        if custom_instruction := custom_instruction.strip():
            return (
                f"{base_instruction}\n\nAdditional instruction:\n{custom_instruction}"
            )
        else:
            return base_instruction
