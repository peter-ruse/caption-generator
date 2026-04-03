from services.base import LLMService
from services.enums import Provider
from services.gemini_service import gemini_service


class LLMServiceFactory:
    _instances = {}

    @classmethod
    def get_service_from_provider(cls, provider: Provider) -> LLMService:
        match provider:
            case Provider.GEMINI:
                if provider not in cls._instances:
                    cls._instances[provider] = gemini_service
                return cls._instances[provider]
            case _:
                raise ValueError(f"Unknown provider: {provider}")
