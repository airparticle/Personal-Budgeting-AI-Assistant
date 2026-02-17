from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App Info
    PROJECT_NAME: str = "Finance AI Assistant"
    API_V1_STR: str = "/api/v1"

    # Database Settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Optional: Full URL override
    DATABASE_URL: Optional[str] = None

    # Security (JWT)
    SECRET_KEY: str  # Generated via `openssl rand -hex 32`
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"


settings = Settings()