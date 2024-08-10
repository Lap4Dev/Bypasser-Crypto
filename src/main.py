import asyncio
import datetime
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.projects.hamster_combat.schedule import hamster_codes_filling_if_necessary
from src.config import settings, logger

hamster_task_lock = asyncio.Lock()


async def scheduled_hamster_task():
    if not hamster_task_lock.locked():
        async with hamster_task_lock:
            min_codes_count = 100
            await hamster_codes_filling_if_necessary(min_codes_count)


async def scheduled_backup_db(bot):
    try:
        if settings.BACKUP_CHANNEL_ID:
            backup_file_name = f'bot_backup_{datetime.datetime.now().strftime("%Y-%m-%d")}.db'

            backup_file = FSInputFile(settings.DB_PATH, filename=backup_file_name)

            await bot.send_document(chat_id=settings.BACKUP_CHANNEL_ID, document=backup_file)
            logger.info(f"Backup file {backup_file_name} successfully sent to channel {settings.BACKUP_CHANNEL_ID}")
        else:
            logger.error('Channel or group ID for backup sending not found')
    except Exception as ex:
        logger.error(f"An error occurred while sending DB backup: {ex}")


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
    scheduler.add_job(scheduled_hamster_task, 'interval', minutes=1)
    scheduler.add_job(scheduled_backup_db,  'cron', hour=0, minute=0, kwargs={'bot': bot})
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
