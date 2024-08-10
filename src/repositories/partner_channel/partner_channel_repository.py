from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import IPartnerChannelRepository
from src.database.models import PartnerChannel
from src.schemas import PartnerChannelSchema
from src.config import logger


class SqlAlchemyPartnerChannelRepository(IPartnerChannelRepository):
    model = PartnerChannel

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_all(self) -> list[PartnerChannelSchema]:
        try:
            result = await self.session.execute(select(self.model))
            channels = result.scalars().all()
            return [PartnerChannelSchema(
                channel_id=channel.channel_id,
                channel_link=channel.channel_link,
                name=channel.name
            ) for channel in channels]
        except Exception as ex:
            logger.error(f'Error while getting partner channels: {ex}')
            return []
