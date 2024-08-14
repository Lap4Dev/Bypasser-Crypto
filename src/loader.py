from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import settings
from src.database.db_helper import DatabaseHelper
from src.database.schemas import DatabaseConfig

db_helper = DatabaseHelper(
    DatabaseConfig(
        url=settings.DB_URL,
        echo=settings.DB_ECHO
    )
)
bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

dp = Dispatcher()
