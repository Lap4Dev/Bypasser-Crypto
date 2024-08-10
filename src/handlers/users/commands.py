from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto

from src.config import constants as c
from src.config import settings
from src.config.constants import CD_MAIN_MENU
from src.config.templates import FIRST_MESSAGE_START, MESSAGE_START
from src.keyboards import inline
from src.repositories import SqlAlchemyUserRepository

router = Router()


@router.callback_query(F.data == CD_MAIN_MENU)
@router.message(CommandStart())
async def start(message: Message | CallbackQuery, session, state: FSMContext):
    await state.clear()
    tg_user = message.from_user

    user_repository = SqlAlchemyUserRepository(session)

    was_created = await user_repository.verify_user(tg_user.id)

    if isinstance(message, Message):
        photo_file = FSInputFile(settings.IMAGES_PATH / (c.WELCOME_IMAGE_NAME if was_created else c.START_IMAGE_NAME))
        await message.answer_photo(
            photo=photo_file,
            caption=FIRST_MESSAGE_START if was_created else MESSAGE_START,
            reply_markup=inline.main_menu
        )
    else:
        photo_file = FSInputFile(settings.IMAGES_PATH / (c.WELCOME_IMAGE_NAME if was_created else c.START_IMAGE_NAME))
        media = InputMediaPhoto(
            media=photo_file,
            caption=FIRST_MESSAGE_START if was_created else MESSAGE_START
        )
        await message.message.edit_media(
            media=media,
            reply_markup=inline.main_menu
        )
