from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiocryptopay import AioCryptoPay

from src.config import settings
from src.database.db_helper import DatabaseHelper
from src.database.schemas import DatabaseConfig
from src.utils.security import Security

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

crypto_bot = AioCryptoPay(
    token=settings.CRYPTO_BOT_API_KEY,
    network=settings.CRYPTO_BOT_NETWORK
)

security = Security(secret_key=settings.SECRET_ENCODE_KEY)
