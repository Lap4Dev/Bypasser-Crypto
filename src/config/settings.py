import os
from pathlib import Path

from aiocryptopay import Networks
from pydantic import SecretStr

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr

    BASE_WEBHOOK_URL: str
    WEBHOOK_PATH: str = '/bot_webhook'
    WEBHOOK_SECRET: str
    WEB_SERVER_PORT: int = 3001
    WEB_SERVER_HOST: str = '0.0.0.0'

    LOG_LEVEL: str = 'DEBUG'
    LOG_FILE_PATH: str | Path = BASE_DIR / 'bot.log'
    IMAGES_PATH: str | Path = BASE_DIR / 'assets'

    DB_NAME: str
    DB_ECHO: bool = True

    CRYPTO_BOT_API_KEY: str
    CRYPTO_BOT_NETWORK: str = Networks.MAIN_NET

    SECRET_ENCODE_KEY: str = 'mysecretkey'

    BACKUP_CHANNEL_ID: int | None
    INSTRUCTION_CHANNEL_ID: int
    BOT_LINK: str
    SUPPORT_LINK: str
    OFFICIAL_CHANNEL_LINK: str
    OFFICIAL_CHAT_LINK: str

    HAMSTER_KEYS_LIMIT_PER_DAY: int = 4

    BLUM_REF_LINK: str = 'https://t.me/BlumCryptoBot/app?startapp=ref_Ae49shKgSM'
    GRASS_REF_LINK: str = 'https://app.getgrass.io/register/?referralCode=hJxVzwJX7vD7CQ5'
    HAMSTER_REF_LINK: str = 'https://t.me/hamster_kombaT_bot/start?startapp=kentId761299691'
    MEMEFI_REF_LINK: str = 'https://t.me/memefi_coin_bot?start=r_fe9aae9648'

    PRODUCTION: bool = False
    CERT_KEY_PATH: str | None = None
    CERT_PEM_PATH: str | None = None

    @property
    def TELEGRAM_WEBHOOK_URL(self) -> str:
        return f'{self.BASE_WEBHOOK_URL}{self.WEBHOOK_PATH}'

    @property
    def crypto_bot_webhook_endpoint(self) -> str:
        return f'/{self.CRYPTO_BOT_API_KEY}'

    @property
    def DB_PATH(self) -> Path:
        return BASE_DIR / self.DB_NAME

    @property
    def DB_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_PATH}"

    @property
    def SYNC_DB_URL(self) -> str:
        return f"sqlite:///{self.DB_PATH}"

    class Config:
        env_file = BASE_DIR / os.getenv('ENV_FILE', '.dev.env')
        env_file_encoding = 'utf-8'


settings = Settings()
if settings.PRODUCTION:
    if not (settings.CERT_PEM_PATH or settings.CERT_KEY_PATH):
        raise Exception("CERT_PEM_PATH and CERT_KEY_PATH required for production")
