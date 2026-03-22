from config import GeminiSettings
from services.base import LLMService
from services.gemini_service import GeminiService
from services.models import Provider


class LLMServiceFactory:
    _instances = dict()

    @classmethod
    def get_service_from_provider(cls, provider: Provider) -> LLMService:
        match provider:
            case Provider.GEMINI:
                settings = GeminiSettings()  # type: ignore
                if provider not in cls._instances:
                    cls._instances[provider] = GeminiService(
                        api_key=settings.raw_api_key
                    )
                return cls._instances[provider]
            case _:
                raise ValueError(f"Unknown provider: {provider}")
