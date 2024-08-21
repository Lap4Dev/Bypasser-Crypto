from sqlalchemy.ext.asyncio import AsyncSession

from src.config import logger
from src.config.constants import PRODUCT_HAMSTER_KOMBAT_CLAIMER
from src.database.models import HamsterClaimer
from src.projects.hamster_combat.auto_claim import process_accounts
from src.repositories import (
    SqlAlchemySubscriptionRepository as SubscriptionRepo,
    SqlAlchemyHamsterClaimerRepository as ClaimerRepo,
    SqlAlchemyConfidentialRepository as ConfidentialRepo,
    SqlAlchemyProductRepository as ProductRepo
)


class ClaimerService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.subs_repo: SubscriptionRepo = SubscriptionRepo(session)
        self.claimer_repo: ClaimerRepo = ClaimerRepo(session)
        self.confidential_repo: ConfidentialRepo = ConfidentialRepo(session)
        self.product_repo: ProductRepo = ProductRepo(session)

    async def get_all_tokens(self) -> list:
        claimers: list[HamsterClaimer] = await self.claimer_repo.get_all_active()
        tokens = []
        product = await self.product_repo.get_by_name(PRODUCT_HAMSTER_KOMBAT_CLAIMER)

        for claimer in claimers:
            subscription = await self.subs_repo.get_subscription(claimer.user_id, product.id)
            if not subscription.is_subscription_active():
                await self.claimer_repo.set_active(claimer.user_id, is_active=False)
                continue
            if claimer.token_id is None:
                continue

            confidential = await self.confidential_repo.get_by_id(claimer.token_id)
            if confidential.value:
                logger.debug(f'Got token of user: [{claimer.user_id}], token_id: [{claimer.token_id}]')
                tokens.append(confidential.value)

        return tokens

    async def claim_all(self):
        tokens = await self.get_all_tokens()
        await process_accounts(tokens)
