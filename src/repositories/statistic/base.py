from abc import ABC, abstractmethod
from typing import Tuple, Any

from src.database.models import TelegramUser, Statistic


class IStatisticRepository(ABC):
    model = None

    @abstractmethod
    async def increment_value(self, user_id: int, name: str) -> int:
        ...

    @abstractmethod
    async def reset_value(self, user_id: int, name: str) -> None:
        ...

    @abstractmethod
    async def get_value(self, user_id: int, name: str) -> int:
        ...

    @abstractmethod
    async def add_value(self, user_id: int, name: str, amount: int) -> int:
        ...

    @abstractmethod
    async def get_or_create(self, user_id: int, name: str) -> Statistic:
        ...
