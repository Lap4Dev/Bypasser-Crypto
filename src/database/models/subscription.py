
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models import TelegramUser, Product


class Subscription(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("telegramusers.user_id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        server_default=func.now()
    )
    end_date: Mapped[datetime] = mapped_column(default=None, nullable=True)
    user: Mapped['TelegramUser'] = relationship("TelegramUser", back_populates="subscriptions")
    product: Mapped['Product'] = relationship("Product", back_populates="subscriptions")

    def __repr__(self):
        return f"<Subscription(user_id={self.user_id}, product_id={self.product_id}, end_date={self.end_date})>"

    def set_end_date(self):
        self.end_date = self.start_date + timedelta(days=self.product.duration_days)

    def is_subscription_active(self) -> bool:
        current_time = datetime.utcnow()

        if self.end_date is None:
            return self.start_date <= current_time

        return self.start_date <= current_time <= self.end_date
