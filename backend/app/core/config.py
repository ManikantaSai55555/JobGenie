from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, case_sensitive=False)

    app_name: str = Field(default="JobScout")
    environment: str = Field(default="development")

    secret_key: str = Field(default="dev-secret-change-me")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60 * 24 * 7)

    database_url: str = Field(default="sqlite:///./jobs.db")
    redis_url: str = Field(default="redis://localhost:6379/0")

    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000", "*"])

    # AI / Matching
    openai_api_key: str | None = None
    embedding_provider: str = Field(default="simple")  # options: simple|openai

    # Aggregation
    aggregation_providers: List[str] = Field(default_factory=lambda: ["remoteok"])  # extendable


settings = Settings()