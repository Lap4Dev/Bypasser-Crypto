from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from src.config.templates import START_COMMAND_DESCRIPTION
from src.config.constants import CMD_START


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command=CMD_START,
            description=START_COMMAND_DESCRIPTION
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeAllPrivateChats())
