"""Central application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings shared by application components."""

    app_name: str = "LinkPlease Assignment"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = (
        "postgresql+asyncpg://linkplease:linkplease@localhost:5432/linkplease"
    )
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> object:
        """Allow comma-separated origins in environment variables."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return one cached settings instance for dependency injection."""
    return Settings()
