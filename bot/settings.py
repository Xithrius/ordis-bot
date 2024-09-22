from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str = ""
    prefix: str = "^"
    environment: str = "production"

    extensions_autoreload_check_interval: int = 5

    internal_api_url: str = "http://localhost:8000"
    internal_api_healthcheck_attempts: int = 5
    internal_api_timeout: float = 5.0

    external_api_timeout: float = 10.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ORDIS_BOT_",
        env_file_encoding="utf-8",
    )


settings = Settings()
