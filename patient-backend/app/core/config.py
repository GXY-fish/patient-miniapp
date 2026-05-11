from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    app_name: str = "stoma-ai-backend"
    env: str = "dev"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:3000,http://localhost:8000"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/stoma_ai"
    redis_url: str = "redis://localhost:6379/0"
    upload_dir: str = "./uploads"
    jwt_secret_key: str = "change-me"
    jwt_access_token_expire_minutes: int = 120

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
