from pydantic import (
    BaseSettings,
    SecretStr
)

from pathlib import Path


class Settings(BaseSettings):
    TELEGRAM_TOKEN: SecretStr
    DOMAIN: str
    WEBHOOK_PATH: str
    BOT_PUBLIC_PORT: int
    PUBLIC_HOST: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_DB: str
    DB_RETRY_LIMIT: int
    DB_RETRY_INTERVAL: int
    ADMIN: int
    COUNT_RECORDS_RER_PAGE: int

    class Config:
        env_file = Path(__file__).parent / '.env'


config = Settings()
