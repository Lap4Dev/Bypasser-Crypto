from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link


async def create_ref_link(bot: Bot, user_id: int):
    return await create_start_link(bot=bot, payload=f"ref_{user_id}")
