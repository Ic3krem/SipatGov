from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Supabase
    DATABASE_URL: str
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # JWT
    SECRET_KEY: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 30
    REFRESH_EXPIRY_DAYS: int = 7

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "ap-southeast-1"

    # Anthropic
    ANTHROPIC_API_KEY: str = ""

    # Storage
    S3_BUCKET_NAME: str = "sipatgov-documents"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # App
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:8081", "exp://localhost:8081"]

    # Request size limit in bytes (default 10MB)
    MAX_REQUEST_SIZE: int = 10 * 1024 * 1024

    # Mock flags (for local dev / testing without external services)
    MOCK_OCR: bool = True
    MOCK_NLP: bool = True

    @model_validator(mode="after")
    def validate_cors_origins(self) -> "Settings":
        """Ensure CORS_ORIGINS is never wildcard and defaults to localhost if empty."""
        if not self.CORS_ORIGINS or "*" in self.CORS_ORIGINS:
            self.CORS_ORIGINS = ["http://localhost:8081", "exp://localhost:8081"]
        return self


settings = Settings()
