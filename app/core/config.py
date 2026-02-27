from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]   # project root (…/project/)
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    SMTP_HOST: str
    SMTP_PORT: int = 465
    SMTP_USER: str
    SMTP_PASS: str
    EMAIL_FROM: str

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
