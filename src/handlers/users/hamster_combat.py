from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from src.callback_queries import HamsterGame
from src.config import settings
from src.config import constants as c
from src.config import templates as t
from src.keyboards import builder, inline
from src.repositories import SqlAlchemyHamsterCodeRepository

router = Router()


@router.callback_query(F.data == c.CD_HAMSTER_KEY)
async def get_hamster_games(query: CallbackQuery):
    photo_file = FSInputFile(settings.IMAGES_PATH / c.HAMSTER_IMAGE_NAME)
    media = InputMediaPhoto(
        media=photo_file,
        caption=t.CHOOSE_HAMSTER_GAME
    )
    await query.message.edit_media(
        media=media,
        reply_markup=builder.get_hamster_games(go_back_to=c.CD_MAIN_MENU)
    )


@router.callback_query(HamsterGame.filter())
async def hamster_game(query: CallbackQuery, callback_data: HamsterGame, session):
    game_id = int(callback_data.game_id)
    hamster_repo = SqlAlchemyHamsterCodeRepository(session)
    hamster_code = await hamster_repo.get_code(game_id)
    if hamster_code is None:
        return await query.answer(t.CODE_NOT_FOUND, show_alert=True)

    photo_file = FSInputFile(settings.IMAGES_PATH / c.HAMSTER_GAMES[game_id-1][2])
    media = InputMediaPhoto(
        media=photo_file,
        caption=t.code_generated_msg(
            hamster_code.code,
            c.HAMSTER_GAMES[game_id-1][1],
            settings.HAMSTER_REF_LINK
        )
    )
    await query.message.edit_media(
        media=media,
        reply_markup=inline.go_back_to(go_to=c.CD_HAMSTER_KEY)
    )
