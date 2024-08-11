from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from src.config import constants as c
from src.config import settings
from src.config import templates as t
from src.keyboards import inline
from src.repositories import SqlAlchemyUserRepository
from src.utils.bot import create_media

router = Router()


@router.callback_query(F.data == c.CD_MAIN_MENU)
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
            caption=t.FIRST_MESSAGE_START if was_created else t.MESSAGE_START,
            reply_markup=inline.main_menu
        )
    else:
        media = create_media(
            settings.IMAGES_PATH / (c.WELCOME_IMAGE_NAME if was_created else c.START_IMAGE_NAME),
            t.FIRST_MESSAGE_START if was_created else t.MESSAGE_START
        )
        await message.message.edit_media(
            media=media,
            reply_markup=inline.main_menu
        )


@router.callback_query(F.data == c.HAMSTER_KOMBAT)
async def hamster_kombat_menu(query: CallbackQuery):
    media = create_media(
        photo_path=(settings.IMAGES_PATH / c.HAMSTER_MENU_IMAGE_NAME),
        caption=t.HAMSTER_KOMBAT_MENU_MSG
    )
    await query.message.edit_media(
        media=media,
        reply_markup=inline.get_hamster_menu(c.CD_MAIN_MENU)
    )


@router.callback_query(F.data == c.INFO)
async def info(query: CallbackQuery):
    media = create_media(settings.IMAGES_PATH / c.INFO_IMAGE_NAME, caption=t.INFO_MSG)
    await query.message.edit_media(
        media=media,
        reply_markup=inline.get_info(c.CD_MAIN_MENU)
    )
