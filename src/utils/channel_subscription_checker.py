from abc import ABC, abstractmethod

from aiogram import Bot
from aiogram.types import ChatMemberLeft, FSInputFile

from src.config import logger, settings
from src.config.constants import GUARD_IMAGE_NAME
from src.config.templates import GUARD_SUBSCRIPTION_NEEDED_MESSAGE
from src.keyboards.builder import get_partner
from src.schemas import PartnerChannelSchema


class IChannelsSubscriptionChecker(ABC):
    @abstractmethod
    async def is_subscribed_to_all(self, bot: Bot, user_id: int) -> bool:
        ...

    @abstractmethod
    async def send_warning_message(self, sending_callback):
        ...


class ChannelSubscriptionChecker:

    def __init__(self, channel_id: int):
        self.channel_id = channel_id

    async def is_user_subscribed_to_channel(self, bot: Bot, user_id: int) -> bool:
        try:
            user_info = await bot.get_chat_member(
                chat_id=self.channel_id, user_id=user_id
            )
        except Exception as ex:
            logger.error(f"Something went wrong while getting chat member: {ex}")
            return False
        else:
            if isinstance(user_info, ChatMemberLeft):
                return False

            return True


class PartnersSubscriptionChecker(IChannelsSubscriptionChecker):
    def __init__(self, channels: list[PartnerChannelSchema]):
        self.channels = channels

    async def is_subscribed_to_all(self, bot: Bot, user_id: int) -> bool:
        for channel in self.channels:
            channel_sub_checker = ChannelSubscriptionChecker(
                channel_id=channel.channel_id
            )
            is_subscribed = await channel_sub_checker.is_user_subscribed_to_channel(bot, user_id)
            if not is_subscribed:
                return False

        return True

    async def send_warning_message(self, sending_callback):
        await sending_callback(
            FSInputFile(settings.IMAGES_PATH / GUARD_IMAGE_NAME),
            caption=GUARD_SUBSCRIPTION_NEEDED_MESSAGE,
            reply_markup=get_partner(self.channels),
        )

    def __str__(self):
        text = ''
        for channel in self.channels:
            text += f'\n[{channel.channel_id}] --- {channel.name}\n'

        return text
