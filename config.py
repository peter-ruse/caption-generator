from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeminiSettings(BaseSettings):
    api_key: SecretStr = Field(validation_alias="GEMINI_API_KEY")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def raw_api_key(self):
        return self.api_key.get_secret_value()


gemini_settings = GeminiSettings()  # type: ignore
