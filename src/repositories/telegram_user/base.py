from abc import ABC, abstractmethod
from typing import Tuple, Any, Sequence

from src.database.models import TelegramUser


class IUserRepository(ABC):
    model = None

    @abstractmethod
    async def get_or_create(self, user_id: int, username: str, first_name: str, last_name: str) -> Tuple[TelegramUser, bool]:
        ...

    @abstractmethod
    async def get_field_value(self, user_id: int, field_name: str) -> Any:
        ...

    @abstractmethod
    async def set_field_value(self, user_id: int, field_name: str, value: bool) -> None:
        ...

    @abstractmethod
    async def is_admin(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def is_banned(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> int:
        ...

    @abstractmethod
    async def get_referral_counts(self, user_id: int) -> Tuple[int, int]:
        ...

    @abstractmethod
    async def verify_user(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def get_all_verified(self) -> Sequence[TelegramUser]:
        ...

    @abstractmethod
    async def get_all_user_ids(self) -> list[TelegramUser]:
        ...
