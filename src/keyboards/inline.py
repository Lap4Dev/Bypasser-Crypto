from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.config.constants import HAMSTER_KEY, CD_HAMSTER_KEY, GO_BACK, REFERRAL_PROGRAM, CD_REFF_PROG

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=HAMSTER_KEY, callback_data=CD_HAMSTER_KEY)],
        [InlineKeyboardButton(text=REFERRAL_PROGRAM, callback_data=CD_REFF_PROG)]
    ]
)


def go_back_to(go_to: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=GO_BACK, callback_data=go_to)],

        ]
    )
