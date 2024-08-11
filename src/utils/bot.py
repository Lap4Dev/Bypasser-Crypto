from aiogram import Bot
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.utils.deep_linking import create_start_link


async def create_ref_link(bot: Bot, user_id: int):
    return await create_start_link(bot=bot, payload=f"ref_{user_id}")


def create_media(photo_path, caption) -> InputMediaPhoto:
    photo_file = FSInputFile(photo_path)
    return InputMediaPhoto(media=photo_file, caption=caption)
