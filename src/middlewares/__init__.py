from aiogram import Dispatcher

from .partners_middleware import PartnersMiddleware
from .db_session_middleware import DbSessionMiddleware
from .loggin_middleware import LoggingMiddleware
from src.utils.channel_subscription_checker import PartnersSubscriptionChecker
from src.loader import db_helper
from src.repositories import SqlAlchemyPartnerChannelRepository


async def setup_middlewares(dp: Dispatcher):

    dp.message.outer_middleware(LoggingMiddleware())
    dp.callback_query.outer_middleware(LoggingMiddleware())

    dp.update.middleware(DbSessionMiddleware(db_helper.session_factory))

    async with db_helper.get_db() as session:
        partner_channels = await SqlAlchemyPartnerChannelRepository(session).get_all()

    partners = PartnersMiddleware(
        partners_checker=PartnersSubscriptionChecker(channels=partner_channels)
    )

    dp.message.outer_middleware(partners)
    dp.callback_query.outer_middleware(partners)


__all__ = (
    "PartnersMiddleware",
    "LoggingMiddleware",
    "DbSessionMiddleware",
    "setup_middlewares"
)
