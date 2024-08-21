from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import logger
from src.database.models import Subscription
from src.repositories import (
    SqlAlchemySubscriptionRepository as SubscriptionRepo,
    SqlAlchemyPaymentRepository as PaymentRepo,
    SqlAlchemyProductRepository as ProductRepo,
)
from src.schemas import PaymentPayload


class SubscriptionService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.subs_repo: SubscriptionRepo = SubscriptionRepo(session)
        self.payment_repo: PaymentRepo = PaymentRepo(session)
        self.product_repo: ProductRepo = ProductRepo(session)

    async def confirm_payment(self, payload: PaymentPayload) -> Subscription | None:
        product = await self.product_repo.get_by_name(product_name=payload.product_name)
        if product is None:
            logger.warning(f'User: [{payload.user_id}] has been paid but product: [{payload.product_name}] not found!')
            return

        start_date = datetime.utcnow()

        subscription = await self.subs_repo.create_or_update_subscription(
            user_id=payload.user_id,
            product_id=product.id,
            start_date=start_date,
            end_date=start_date + timedelta(days=product.duration_days)
        )

        if subscription is None:
            logger.warning(f'User: [{payload.user_id}] has been paid but subscription not created!')
            return

        payment = await self.payment_repo.create_payment(
            invoice_id=payload.invoice_id,
            user_id=payload.user_id,
            subscription_id=subscription.id,
            payment_service=payload.payment_service,
            amount=payload.amount
        )

        if payment is None:
            logger.warning(
                f'User: [{payload.user_id}] has been paid but payment not created with sub_id: [{subscription.id}]!')
            return

        logger.info(
            f'Subscription successfully activated for User: [{payload.user_id}] for Product: [{payload.product_name}]')

        return subscription

    async def is_subscribe(self, user_id: int, product_name: str) -> bool:
        product = await self.product_repo.get_by_name(product_name=product_name)
        if not product:
            return False

        subscription = await self.subs_repo.get_subscription(user_id, product.id)

        if not subscription:
            return False

        return subscription.is_subscription_active()

    async def get_subscription(self, user_id: int, product_name: str) -> Subscription | None:
        product = await self.product_repo.get_by_name(product_name=product_name)
        if not product:
            return

        subscription = await self.subs_repo.get_subscription(user_id, product.id)

        return subscription
