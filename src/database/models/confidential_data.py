from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING
from src.database.models import Base

if TYPE_CHECKING:
    from .telegram_user import TelegramUser


class ConfidentialData(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("telegramusers.user_id"), nullable=False)
    tg_query_hashed: Mapped[str] = mapped_column(String(1024))

    user: Mapped["TelegramUser"] = relationship("TelegramUser", back_populates="confidential_data")
