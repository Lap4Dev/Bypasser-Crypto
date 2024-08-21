from abc import ABC, abstractmethod
from datetime import datetime

from src.database.models import Subscription


class ISubscriptionRepository(ABC):
    model = None

    @abstractmethod
    async def create_or_update_subscription(self, user_id: int, product_id: int, start_date: datetime,
                                            end_date: datetime) -> Subscription | None:
        ...

    @abstractmethod
    async def get_subscription(self, user_id: int, product_id: int) -> Subscription | None:
        ...

