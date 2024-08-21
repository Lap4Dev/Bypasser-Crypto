from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ConfidentialData
from .base import IConfidentialRepository
from ...config import logger


class SqlAlchemyConfidentialRepository(IConfidentialRepository):
    model: ConfidentialData = ConfidentialData

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def find_or_create(self, user_id: int, name: str, value: str) -> ConfidentialData:
        # Ищем записи с соответствующим user_id и name
        result = await self.session.execute(
            select(self.model).where(
                self.model.user_id == user_id,
                self.model.name == name
            )
        )
        datas: list[ConfidentialData] = list(result.scalars().all())

        # Если найдено, проверяем совпадение значения
        for data in datas:
            if data.value == value:
                return data

        # Если значение не совпадает, создаем новый объект
        if datas and all(data.value != value for data in datas):
            new_data = self.model(user_id=user_id, name=name, value=value)
            self.session.add(new_data)
            await self.session.commit()
            return new_data

        # Если ничего не найдено, создаем новый объект
        new_data = self.model(user_id=user_id, name=name, value=value)
        self.session.add(new_data)
        await self.session.commit()
        return new_data

    async def create_or_update(self, user_id: int, name: str, value: str) -> ConfidentialData | None:
        try:
            result = await self.session.execute(
                select(self.model).where(
                    self.model.user_id == user_id,
                    self.model.name == name
                )
            )
            instance: ConfidentialData = result.scalars().first()

            if not instance:
                new_instance = self.model(user_id=user_id, name=name, value=value)
                self.session.add(new_instance)
                await self.session.commit()
                return new_instance

            instance.value = value
            self.session.add(instance)
            await self.session.commit()
            return instance

        except Exception as ex:
            logger.error(f'Error while create_or_update confidential for user_id: [{user_id}] name: [{name}]: {ex}')

    async def get_by_id(self, confidential_id: int) -> ConfidentialData | None:
        result = await self.session.execute(
            select(self.model).where(
                self.model.id == confidential_id,
            )
        )
        return result.scalars().first()
