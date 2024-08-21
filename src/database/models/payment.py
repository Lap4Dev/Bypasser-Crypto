
from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models import TelegramUser, Subscription


class PaymentStatus(Enum):
    confirm = 'confirm'
    pending = 'pending'
    canceled = 'canceled'

# Payment -> Subscription -> Product


class Payment(Base):
    invoice_id: Mapped[str] = mapped_column(String(128))
    user_id: Mapped[int] = mapped_column(ForeignKey("telegramusers.user_id"), nullable=False)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"), nullable=True)
    amount: Mapped[float] = mapped_column(default=0, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.confirm)
    payment_service: Mapped[str] = mapped_column(String(32), default='')
    user: Mapped['TelegramUser'] = relationship("TelegramUser", back_populates="payments")
    subscription: Mapped['Subscription'] = relationship("Subscription")

    def __repr__(self):
        return f"<Payment(user_id={self.user_id}, amount={self.amount})>"
