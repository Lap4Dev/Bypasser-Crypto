import os
from pathlib import Path

from pydantic import SecretStr

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    LOG_FILE_PATH: str | Path = BASE_DIR / 'bot.log'
    IMAGES_PATH: str | Path = BASE_DIR / 'src' / 'assets'
    DB_ECHO: bool = True
    BACKUP_CHANNEL_ID: int | None

    SUPPORT_LINK: str
    OFFICIAL_CHANNEL_LINK: str
    OFFICIAL_CHAT_LINK: str

    HAMSTER_KEYS_LIMIT_PER_DAY: int = 4

    LOG_LEVEL: str = 'INFO'
    BLUM_REF_LINK: str = 'https://t.me/BlumCryptoBot/app?startapp=ref_Ae49shKgSM'
    GRASS_REF_LINK: str = 'https://app.getgrass.io/register/?referralCode=hJxVzwJX7vD7CQ5'
    HAMSTER_REF_LINK: str = 'https://t.me/hamster_kombaT_bot/start?startapp=kentId761299691'
    MEMEFI_REF_LINK: str = 'https://t.me/memefi_coin_bot?start=r_fe9aae9648'

    @property
    def DB_PATH(self) -> Path:
        return BASE_DIR / 'bot.db'

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
