from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Subscription
from .base import ISubscriptionRepository
from src.config import logger


class SqlAlchemySubscriptionRepository(ISubscriptionRepository):
    model: Subscription = Subscription

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create_or_update_subscription(self, user_id: int, product_id: int, start_date: datetime,
                                            end_date: datetime) -> Subscription | None:
        try:
            # Перевірка наявності існуючої підписки
            subscription = await self.get_subscription(user_id, product_id)

            if subscription:
                # Оновлення існуючої підписки
                subscription.start_date = start_date
                subscription.end_date = end_date
                await self.session.commit()
            else:
                # Створення нової підписки
                subscription = self.model(
                    user_id=user_id,
                    product_id=product_id,
                    start_date=start_date,
                    end_date=end_date
                )
                self.session.add(subscription)
                await self.session.commit()

            return subscription

        except SQLAlchemyError as ex:
            logger.error(
                f'Error while creating or updating subscription(user_id={user_id}, product_id={product_id}): {ex}')
            await self.session.rollback()
            return None

    async def get_subscription(self, user_id: int, product_id: int) -> Subscription | None:
        result = await self.session.execute(
            select(self.model).where(
                self.model.user_id == user_id,
                self.model.product_id == product_id
            )
        )
        return result.scalars().first()
