from abc import ABC, abstractmethod

from src.database.models import ConfidentialData


class IConfidentialRepository(ABC):
    model = None

    @abstractmethod
    async def find_or_create(self, user_id: int, name: str, value: str) -> ConfidentialData:
        ...

    @abstractmethod
    async def create_or_update(self, user_id: int, name: str, value: str) -> ConfidentialData | None:
        ...
