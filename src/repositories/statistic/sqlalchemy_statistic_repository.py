from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Statistic
from .base import IStatisticRepository


class SqlAlchemyStatisticRepository(IStatisticRepository):
    model = Statistic

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def increment_value(self, user_id: int, name: str) -> int:
        statistic = await self.get_or_create(user_id, name)
        statistic.value += 1
        await self.session.commit()
        return statistic.value

    async def decrement_value(self, user_id: int, name: str) -> int:
        statistic = await self.get_or_create(user_id, name)
        if statistic.value > 0:
            statistic.value -= 1

        await self.session.commit()
        return statistic.value

    async def reset_value(self, user_id: int, name: str) -> None:
        statistic = await self.get_or_create(user_id, name)
        statistic.value = 0
        await self.session.commit()

    async def get_value(self, user_id: int, name: str) -> int:
        statistic = await self.get_or_create(user_id, name)
        return statistic.value

    async def add_value(self, user_id: int, name: str, amount: int) -> int:
        statistic = await self.get_or_create(user_id, name)
        statistic.value += amount
        await self.session.commit()
        return statistic.value

    async def get_or_create(self, user_id: int, name: str) -> Statistic:
        stmt = select(Statistic).where(Statistic.user_id == user_id, Statistic.name == name)
        try:
            statistic = (await self.session.execute(stmt)).scalars().first()
            if statistic is None:
                raise NoResultFound
        except NoResultFound:
            statistic = Statistic(user_id=user_id, name=name, value=0)
            self.session.add(statistic)
            await self.session.commit()
            await self.session.refresh(statistic)
        return statistic

    async def reset_all_by_name(self, name: str) -> None:
        stmt = (
            update(Statistic)
            .where(Statistic.name == name)
            .values(value=0)
        )
        await self.session.execute(stmt)
        await self.session.commit()
