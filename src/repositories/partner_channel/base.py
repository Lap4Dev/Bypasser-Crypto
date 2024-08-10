from abc import ABC, abstractmethod

from src.schemas import PartnerChannelSchema


class IPartnerChannelRepository(ABC):
    model = None

    @abstractmethod
    async def get_all(self) -> list[PartnerChannelSchema]:
        ...

