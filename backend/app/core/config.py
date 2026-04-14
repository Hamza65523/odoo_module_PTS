from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "PTS Backend"
    environment: str = "dev"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    database_url: str = "sqlite:///./pts_backend.db"

    jwt_secret_key: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    api_key: str = "change_me_api_key"
    cors_origins: str = ""

    encryption_key: str = ""

    pts_base_url: str = "https://c33d-2a02-ce0-1802-cedd-4cd4-20be-e317-ec4e.ngrok-free.app/jsonPTS"
    pts_username: str = "admin"
    pts_password: str = "admin"
    pts_auth_mode: str = "basic"
    pts_verify_ssl: bool = False
    poll_interval_seconds: int = 10

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
