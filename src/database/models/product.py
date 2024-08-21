from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .subscription import Subscription


class Product(Base):
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    price_in_usd: Mapped[float] = mapped_column(nullable=False, default=0)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False, default=21)

    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="product")

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price_in_usd}, duration_days={self.duration_days})>"
