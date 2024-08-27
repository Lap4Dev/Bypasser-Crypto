from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.callback_data import HamsterGame
from src.config import constants as c
from src.config import settings
from src.config import templates as t
from src.keyboards import builder, inline
from src.repositories import SqlAlchemyHamsterCodeRepository, SqlAlchemyStatisticRepository, SqlAlchemyUserRepository
from src.utils.bot import create_ref_link, create_media

router = Router()


async def get_keys_limit(user_repo, statistic_repo, user_id, game_id):
    total_referrals_count, active_referrals_count = await user_repo.get_referral_counts(user_id)
    keys_used = await statistic_repo.get_value(user_id, c.DB_STATISTIC_HAMSTER_GAMES[game_id])
    keys_limit = settings.HAMSTER_KEYS_LIMIT_PER_DAY + active_referrals_count * 2
    return keys_used, keys_limit


async def send_keys_limit_message(query: CallbackQuery, keys_used: int, keys_limit: int):
    media = create_media(settings.IMAGES_PATH / c.ACCESS_CARD_IMAGE_NAME, t.keys_limit_msg(
        ref_link=await create_ref_link(query.bot, query.from_user.id),
        keys_used=keys_used,
        keys_limit=keys_limit
    ))
    await query.message.edit_media(media=media, reply_markup=inline.go_back_to(go_to=c.CD_HAMSTER_KEY))


def find_game_by_id(game_id):
    return next((game for game in c.HAMSTER_GAMES if game[0] == game_id), None)


@router.callback_query(F.data == c.CD_HAMSTER_KEY)
async def get_hamster_games(query: CallbackQuery):
    media = create_media(settings.IMAGES_PATH / c.HAMSTER_IMAGE_NAME, t.CHOOSE_HAMSTER_GAME)
    await query.message.edit_media(media=media, reply_markup=builder.get_hamster_games(go_back_to=c.HAMSTER_KOMBAT))


@router.callback_query(HamsterGame.filter())
async def hamster_game(query: CallbackQuery, callback_data: HamsterGame, session):
    user_id = query.from_user.id
    game_id = int(callback_data.game_id)

    user_repo = SqlAlchemyUserRepository(session)
    statistic_repo = SqlAlchemyStatisticRepository(session)

    keys_used, keys_limit = await get_keys_limit(user_repo, statistic_repo, user_id, game_id)

    if keys_used >= keys_limit:
        return await send_keys_limit_message(query, keys_used=keys_used, keys_limit=keys_limit)

    hamster_repo = SqlAlchemyHamsterCodeRepository(session)
    hamster_code = await hamster_repo.get_code(game_id)

    if hamster_code is None:
        return await query.answer(t.CODE_NOT_FOUND, show_alert=True)

    keys_used = await statistic_repo.increment_value(user_id, c.DB_STATISTIC_HAMSTER_GAMES[game_id])
    game = find_game_by_id(game_id)
    media = create_media(
        settings.IMAGES_PATH / game[2],
        t.code_generated_msg(hamster_code.code, game[1], settings.HAMSTER_REF_LINK,
                             keys_used=keys_used, keys_limit=keys_limit)
    )
    await query.message.edit_media(media=media, reply_markup=inline.go_back_to(go_to=c.CD_HAMSTER_KEY))
