from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models.base_model import Base

if TYPE_CHECKING:
    from .telegram_user import TelegramUser


class Statistic(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("telegramusers.user_id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["TelegramUser"] = relationship("TelegramUser", back_populates="statistics")
