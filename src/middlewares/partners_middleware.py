from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.payload import decode_payload

from src.config import logger
from src.config.constants import CHECK_SUBSCRIPTION, CMD_START
from src.utils.channel_subscription_checker import IChannelsSubscriptionChecker
from src.repositories import SqlAlchemyUserRepository


async def process_user(message: Message, session) -> bool:
    tg_user = message.from_user
    referrer_id = None

    if " " in message.text:
        payload = message.text.split(" ", 1)[1]
    else:
        payload = ""

    if payload.startswith("ref_"):
        referrer_id = payload.split("_")[1]
        if referrer_id.isdigit():
            referrer_id = int(referrer_id)

    user_repo = SqlAlchemyUserRepository(session)
    _, was_created = await user_repo.get_or_create(
        user_id=tg_user.id,
        username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        referrer_id=referrer_id
    )

    return was_created


class PartnersMiddleware(BaseMiddleware):
    def __init__(self, partners_checker: IChannelsSubscriptionChecker):
        super().__init__()
        self.partners_checker = partners_checker

        logger.info(f'Initialize partners channels: {self.partners_checker}')

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        bot = data.get("bot")

        chat_type = event.message.chat.type if isinstance(event, CallbackQuery) else event.chat.type
        if chat_type != ChatType.PRIVATE:
            return

        is_member = await self.partners_checker.is_subscribed_to_all(
            bot=bot, user_id=event.from_user.id
        )
        if not is_member:
            if isinstance(event, Message):
                if CMD_START in event.text:
                    await process_user(event, data.get('session'))

                return await self.partners_checker.send_warning_message(event.answer_photo)
            if isinstance(event, CallbackQuery):
                if event.data == CHECK_SUBSCRIPTION:
                    return await handler(event, data)
                try:
                    await event.message.delete()
                except:
                    ...
                return await self.partners_checker.send_warning_message(event.message.answer_photo)

        return await handler(event, data)
