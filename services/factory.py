from services.base import LLMService
from services.enums import Provider
from services.gemini_service import gemini_service


class LLMServiceFactory:
    @classmethod
    def get_service_from_provider(cls, provider: Provider) -> LLMService:
        match provider:
            case Provider.GEMINI:
                return gemini_service
            case _:
                raise ValueError(f"Unknown provider: {provider}")
