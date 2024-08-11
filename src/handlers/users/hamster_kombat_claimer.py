from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.config import constants as c, settings
from src.config import templates as t
from src.keyboards import inline
from src.utils.bot import create_media

router = Router()


@router.callback_query(F.data == c.CD_AUTO_HMSTR_CLAIMER)
async def hamster_claimer_menu(query: CallbackQuery):
    media = create_media(settings.IMAGES_PATH / c.AUTO_CLAIMER_HAMSTER_IMAGE_NAME, t.HAMSTER_CLAIMER_DESCRIPTION)
    await query.message.edit_media(
        media=media,
        reply_markup=inline.get_hamster_auto_claimer_menu(c.HAMSTER_KOMBAT)
    )


@router.callback_query(F.data == c.CD_RUN_AUTO_BOT)
async def run_auto_bot(query: CallbackQuery):
    return await query.answer('На стадії розробки. Незабаром буде доступно!', show_alert=True)

    await query.message.edit_caption(
        caption=t.AUTO_CLAIMER_PAYMENT_EXPLANATION,
        reply_markup=inline.get_purchase_subscription(
            1, 1, c.CD_AUTO_HMSTR_CLAIMER
        )
    )
