from aiogram import Bot
from aiogram.types import InputMediaPhoto, FSInputFile, Message, CallbackQuery, ChatInviteLink
from aiogram.utils.deep_linking import create_start_link

from src.config import settings
from src.config.constants import ERROR_IMAGE_NAME
from src.config.templates import subscription_successfully_activated
from src.database.models import Subscription
from src.keyboards.inline import get_support
from src.loader import bot


async def create_ref_link(bot: Bot, user_id: int):
    return await create_start_link(bot=bot, payload=f"ref_{user_id}")


async def create_invite_link(bot: Bot, chat_id: int) -> str | None:
    try:
        invite_link: ChatInviteLink = await bot.create_chat_invite_link(
            chat_id=chat_id,
            member_limit=1,
        )

        return invite_link.invite_link

    except Exception:
        return None


def create_media(photo_path, caption) -> InputMediaPhoto:
    photo_file = FSInputFile(photo_path)
    return InputMediaPhoto(media=photo_file, caption=caption)


async def send_error_media(tg_object: Message | CallbackQuery, caption: str):
    photo_path = settings.IMAGES_PATH / ERROR_IMAGE_NAME
    media_file = FSInputFile(photo_path)
    markup = get_support()

    if isinstance(tg_object, Message):
        return await tg_object.answer_photo(
            photo=media_file,
            caption=caption,
            reply_markup=markup
        )

    try:
        await tg_object.message.edit_media(
            media=create_media(photo_path, caption),
            reply_markup=markup
        )
    except:
        await tg_object.message.answer_photo(
            photo=media_file,
            caption=caption,
            reply_markup=markup
        )


async def send_message_after_success_subscription(user_id: int, product_name: str, subscription: Subscription, session):
    await bot.send_message(
        chat_id=user_id,
        text=subscription_successfully_activated(product_name, subscription),
    )
