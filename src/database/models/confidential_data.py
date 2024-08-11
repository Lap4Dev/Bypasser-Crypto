from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING
from src.database.models import Base

if TYPE_CHECKING:
    from .telegram_user import TelegramUser


class ConfidentialData(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("telegramusers.user_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(32))
    value: Mapped[str] = mapped_column(String(2048), nullable=False, default='')
    user: Mapped["TelegramUser"] = relationship("TelegramUser", back_populates="confidential_data")
