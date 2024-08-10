from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import Base


class TelegramUser(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True, default=None)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(default=False)
    referrer_id: Mapped[int] = mapped_column(nullable=True, default=None)
    is_verified: Mapped[bool] = mapped_column(nullable=True, default=False)

    statistics: Mapped[list["Statistic"]] = relationship("Statistic", back_populates="user")
