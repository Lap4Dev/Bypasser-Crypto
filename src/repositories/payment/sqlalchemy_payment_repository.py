from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Payment
from .base import IPaymentRepository
from src.config import logger


class SqlAlchemyPaymentRepository(IPaymentRepository):
    model: Payment = Payment

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create_payment(
            self, user_id: int,
            subscription_id: int,
            amount: float,
            payment_service: str,
            invoice_id: str
    ) -> Payment | None:
        try:
            instance = self.model(
                user_id=user_id,
                subscription_id=subscription_id,
                amount=amount,
                payment_service=payment_service,
                invoice_id=invoice_id
            )
            self.session.add(instance)
            await self.session.commit()
            return instance
        except Exception as ex:
            logger.error(f'Error while creating payment (user_id={user_id}, subscription_id={subscription_id}): {ex}')
            return None
