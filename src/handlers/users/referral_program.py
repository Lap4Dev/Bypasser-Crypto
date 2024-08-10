from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.deep_linking import create_start_link

from src.config import settings
from src.config.constants import CD_REFF_PROG, CD_MAIN_MENU, REFERRAL_PROGRAM_IMAGE_NAME
from src.config.templates import referral_info_msg
from src.keyboards import inline
from src.repositories import SqlAlchemyUserRepository

router = Router()


@router.callback_query(F.data == CD_REFF_PROG)
async def referral_program(query: CallbackQuery, session):
    user_id = query.from_user.id
    user_repo = SqlAlchemyUserRepository(session)

    referral_link = await create_start_link(bot=query.bot, payload=f"ref_{user_id}")
    photo_file = FSInputFile(settings.IMAGES_PATH / REFERRAL_PROGRAM_IMAGE_NAME)
    media = InputMediaPhoto(
        media=photo_file,
        caption=referral_info_msg(
            referral_link,
            await user_repo.get_referral_count_of(user_id)
        )
    )
    await query.message.edit_media(
        media=media,
        reply_markup=inline.go_back_to(go_to=CD_MAIN_MENU)
    )

    await query.answer()
