from typing import Tuple

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import logger
from src.database.models import HamsterClaimer


class SqlAlchemyHamsterClaimerRepository:
    model: HamsterClaimer = HamsterClaimer

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_or_create(self, user_id: int) -> Tuple[HamsterClaimer, bool]:

        try:
            result = await self.session.execute(select(self.model).filter_by(user_id=user_id))

            instance = result.scalars().first()

            if not instance:
                raise NoResultFound()

            was_created = False

        except NoResultFound:

            instance = self.model(user_id=user_id)
            self.session.add(instance)
            await self.session.commit()
            was_created = True

        return instance, was_created

    async def set_token_id(self, user_id: int, token_id: int) -> bool:
        try:
            claimer, _ = await self.get_or_create(user_id)
            claimer.token_id = token_id
            self.session.add(claimer)
            await self.session.commit()
            return True
        except Exception as ex:
            logger.error(f'Error while setting token_id: [{token_id}] for user_id: [{user_id}]: {ex}')
            return False

    async def set_active(self, user_id: int, is_active: bool = False):
        try:
            claimer, _ = await self.get_or_create(user_id)
            claimer.is_active = is_active
            self.session.add(claimer)
            await self.session.commit()
            return True
        except Exception as ex:
            logger.error(f'Error while setting active status for user_id: [{user_id}]: {ex}')
            return False

    async def get_all_active(self) -> list[HamsterClaimer]:
        result = await self.session.execute(
            select(self.model).where(
                self.model.is_active.is_(True)
            )
        )
        return list(result.scalars().all())
