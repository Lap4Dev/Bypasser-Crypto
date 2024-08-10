import asyncio
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.schedule_tasks import setup_schedule_tasks

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings, logger


async def on_startup():
    logger.info('Bot successfully started!')


async def on_shutdown():
    logger.info('Bot shutdown!')


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    from src.utils.bot_commands import set_commands
    await set_commands(bot)

    dp = Dispatcher()

    from src.middlewares import setup_middlewares
    await setup_middlewares(dp)

    from src.handlers import register_routers
    dp.include_routers(register_routers())

    await bot.delete_webhook(drop_pending_updates=True)

    scheduler = AsyncIOScheduler()
    setup_schedule_tasks(scheduler, bot)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
