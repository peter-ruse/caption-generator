from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    env: str = Field(validation_alias="ENV")

    # for authentication
    google_client_id: str = Field(validation_alias="GOOGLE_CLIENT_ID")
    google_client_secret: SecretStr = Field(validation_alias="GOOGLE_CLIENT_SECRET")
    google_discovery_url: str = Field(
        default="https://accounts.google.com/.well-known/openid-configuration",
        validation_alias="GOOGLE_DISCOVERY_URL",
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def raw_google_client_secret(self):
        return self.google_client_secret.get_secret_value()


class GeminiSettings(BaseSettings):
    api_key: SecretStr = Field(validation_alias="GEMINI_API_KEY")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def raw_api_key(self):
        return self.api_key.get_secret_value()


class PostgresqlSettings(BaseSettings):
    user: str = Field(validation_alias="POSTGRES_USER")
    password: SecretStr = Field(validation_alias="POSTGRES_PASSWORD")
    host: str = Field(validation_alias="POSTGRES_HOST")
    port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    database: str = Field(validation_alias="POSTGRES_DATABASE")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def raw_password(self):
        return self.password.get_secret_value()


class JWTSettings(BaseSettings):
    secret_key: SecretStr = Field(validation_alias="SECRET_KEY")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def raw_secret_key(self):
        return self.secret_key.get_secret_value()


app_settings = AppSettings()  # type: ignore
gemini_settings = GeminiSettings()  # type: ignore
postgresql_settings = PostgresqlSettings()  # type: ignore
jwt_settings = JWTSettings()  # type: ignore
