from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import Base
if TYPE_CHECKING:
    from .statistic import Statistic
    from .confidential_data import ConfidentialData
    from .subscription import Subscription
    from .payment import Payment


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
    confidential_data: Mapped["ConfidentialData"] = relationship("ConfidentialData", back_populates="user")
    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="user")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="user")
