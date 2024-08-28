import asyncio
import datetime

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import settings, logger
from src.config.constants import DB_STATISTIC_HAMSTER_GAMES
from src.loader import db_helper
from src.projects.hamster_combat.schedule import hamster_codes_filling_if_necessary
from src.repositories import (
    SqlAlchemyStatisticRepository,
    SqlAlchemyUserRepository,
    SqlAlchemyPartnerChannelRepository
)
from src.services.claimer_service import ClaimerService

hamster_task_lock = asyncio.Lock()
hamster_claimer_lock = asyncio.Lock()


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


async def scheduled_reset_keys_used():
    try:
        async with db_helper.get_db() as session:
            stat_repo = SqlAlchemyStatisticRepository(session)

            for game_id, db_field in DB_STATISTIC_HAMSTER_GAMES.items():
                await stat_repo.reset_all_by_name(db_field)

    except Exception as ex:
        logger.error(f'Reset keys used error: {ex}')


async def update_verification_status(bot: Bot) -> None:
    """
    Обновляет статус is_verified для всех пользователей в базе данных.
    Если пользователь больше не подписан на канал, его статус is_verified устанавливается в False.
    """

    try:
        count_of_un_verified_changes = 0
        async with db_helper.get_db() as session:
            user_repo = SqlAlchemyUserRepository(session)
            partners_repo = SqlAlchemyPartnerChannelRepository(session)
            partners = await partners_repo.get_all()
            verified_users = await user_repo.get_all_verified()
            for user in verified_users:
                for partner in partners:
                    try:
                        member = await bot.get_chat_member(partner.channel_id, user.user_id)
                        if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                            await user_repo.set_field_value(user.user_id, 'is_verified', False)
                            count_of_un_verified_changes += 1
                    except Exception as e:
                        await user_repo.set_field_value(user.user_id, 'is_verified', False)
                        count_of_un_verified_changes += 1
                        logger.error(f"Error while checking user {user.user_id}: {e}")
        logger.info(f'Updating verification status has been ended. Total updated: {count_of_un_verified_changes}')
    except Exception as ex:
        logger.error(f'Error while update_verification_status: {ex}')


async def hamster_claimer():
    if not hamster_claimer_lock.locked():
        async with hamster_claimer_lock:
            async with db_helper.get_db() as session:
                claimer_service = ClaimerService(session)
                await claimer_service.claim_all()


def setup_schedule_tasks(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.add_job(scheduled_hamster_task, 'interval', minutes=1)
    scheduler.add_job(hamster_claimer, 'interval', hours=3)
    scheduler.add_job(scheduled_reset_keys_used, 'cron', hour=0, minute=0)
    scheduler.add_job(scheduled_backup_db, 'cron', hour=1, minute=0, kwargs={'bot': bot})
    scheduler.add_job(update_verification_status, 'cron', hour=2, minute=0, kwargs={'bot': bot})
    logger.info('Jobs successfully initialized !')
