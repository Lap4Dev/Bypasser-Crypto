import asyncio
import datetime

from aiogram import Bot
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import settings, logger
from src.projects.hamster_combat.schedule import hamster_codes_filling_if_necessary

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


def setup_schedule_tasks(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.add_job(scheduled_hamster_task, 'interval', minutes=1)
    scheduler.add_job(scheduled_backup_db, 'cron', hour=0, minute=0, kwargs={'bot': bot})
    logger.info('Jobs successfully initialized !')
