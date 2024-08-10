from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from src.config.constants import CHECK_SUBSCRIPTION
from src.config.templates import HANDLER_NOT_FOUND, GUARD_CHECK_SUB
from src.handlers.users.commands import start
from src.repositories import SqlAlchemyPartnerChannelRepository
from src.utils.channel_subscription_checker import PartnersSubscriptionChecker

router = Router()


@router.callback_query(F.data == CHECK_SUBSCRIPTION)
async def check_subscription(query: CallbackQuery, session, bot, state):
    partner_channels = await SqlAlchemyPartnerChannelRepository(session).get_all()
    subs_checker = PartnersSubscriptionChecker(channels=partner_channels)
    is_subscribed = await subs_checker.is_subscribed_to_all(bot, user_id=query.from_user.id)

    if is_subscribed:
        return await start(query, session=session, state=state)
    else:
        return await query.answer(GUARD_CHECK_SUB)


@router.message()
async def handle_other(message: Message, bot: Bot):
    await message.answer(HANDLER_NOT_FOUND)
