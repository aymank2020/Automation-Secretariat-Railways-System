from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "sqlite:///./railways_hr.db"
    SECRET_KEY: str = Field(..., min_length=32, description="JWT signing key. Set via env. Generate: openssl rand -hex 64")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    UPLOAD_DIR: str = "./uploads"

    # Comma-separated list of allowed origins for CORS. Use the `allow_origins` property to read.
    ALLOW_ORIGINS: str = "http://localhost:5173"

    INITIAL_ADMIN_USERNAME: str = "admin"
    INITIAL_ADMIN_PASSWORD: str | None = None

    @property
    def allow_origins(self) -> list[str]:
        return [s.strip() for s in self.ALLOW_ORIGINS.split(",") if s.strip()]


settings = Settings()
