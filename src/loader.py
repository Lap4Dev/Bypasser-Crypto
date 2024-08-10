from src.config import settings
from src.database.db_helper import DatabaseHelper
from src.database.schemas import DatabaseConfig

db_helper = DatabaseHelper(
    DatabaseConfig(
        url=settings.DB_URL,
        echo=settings.DB_ECHO
    )
)
