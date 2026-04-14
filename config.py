from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    env: str = Field(validation_alias="ENV")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GeminiSettings(BaseSettings):
    api_key: SecretStr = Field(validation_alias="GEMINI_API_KEY")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def raw_api_key(self):
        return self.api_key.get_secret_value()


class PostgresqlSettings(BaseSettings):
    url: str = Field(validation_alias="POSTGRES_URL")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def raw_url(self):
        return self.url


app_settings = AppSettings()  # type: ignore
gemini_settings = GeminiSettings()  # type: ignore
postgresql_settings = PostgresqlSettings()  # type: ignore
