from core.enums import CaptionStyle, SocialMediaPlatform


class PromptManager:
    @classmethod
    def build_prompt(
        cls,
        title: str,
        text: str,
        link: str,
        caption_style: CaptionStyle,
        custom_instruction: str,
    ) -> str:
        base_prompt = (
            f"Generate a caption based on the following article details.\n\n"
            f"Title: {title}\n"
            f"Link: {link}\n"
            f"Article Content: {text}\n\n"
            f"Constraint: Ensure the total length of the caption is "
            f"approximately {caption_style.value.length_in_sentences} sentences, "
            f"and that the final paragraph explicitly includes the link {link}"
        )

        if custom_instruction := custom_instruction.strip():
            return f"{base_prompt}\n\n{custom_instruction}"
        else:
            return base_prompt

    @classmethod
    def build_system_instruction(
        cls, social_media_platform: SocialMediaPlatform
    ) -> str:
        return (
            "Act as a professional social media strategist catering mostly to Australian tourists in Bali.\n"
            "Don't make any references to Australia or Australians unless specifically asked to.\n"
            "Output only the requested content, and append a separate line at the very end "
            "with a space-separated list of suggested relevant and trending hashtags prefixed by 'TAGS:'.\n"
            "Do NOT include introductions, explanations, multiple options, or conversational filler.\n"
            "Adhere strictly to the specified number of sentences, sometimes stated as a range; "
            "e.g., '1-2 sentences' means at least one but not more than two sentences.\n"
            "Be expressive and lively without being verbose; feel free to use emojis where appropriate.\n"
            "ALWAYS output captions in the following form: a single engaging question about the topic, "
            "as a standalone paragraph, followed by a short informative paragraph on the topic consisting of 1-2 sentences, "
            "followed by a one-sentence paragraph directing people to the provided link, "
            "always making sure to put blank lines between paragraphs.\n"
            f"Adhere to {social_media_platform}'s specific character limits and cultural tone."
        )
