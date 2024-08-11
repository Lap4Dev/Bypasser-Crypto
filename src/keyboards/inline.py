from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.callback_data import Subscription
from src.config import constants as c, settings
from src.config import templates as t

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=c.HAMSTER_KOMBAT, callback_data=c.HAMSTER_KOMBAT)],
        # [InlineKeyboardButton(text=c.HAMSTER_KEY, callback_data=c.CD_HAMSTER_KEY)],
        # [InlineKeyboardButton(text=c.AUTO_HAMSTER_CLAIMER, callback_data=c.CD_AUTO_HMSTR_CLAIMER)],
        [InlineKeyboardButton(text=c.REFERRAL_PROGRAM, callback_data=c.CD_REFF_PROG)],
        [InlineKeyboardButton(text=c.INFO, callback_data=c.INFO)]
    ]
)


def go_back_btn(go_to: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=c.GO_BACK, callback_data=go_to)


def go_back_to(go_to: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [go_back_btn(go_to)],
        ]
    )


def get_hamster_menu(go_to: str = c.CD_MAIN_MENU):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c.HAMSTER_KEY, callback_data=c.CD_HAMSTER_KEY)],
            [InlineKeyboardButton(text=c.AUTO_HAMSTER_CLAIMER, callback_data=c.CD_AUTO_HMSTR_CLAIMER)],
            [go_back_btn(go_to)]
        ]
    )


def get_hamster_auto_claimer_menu(go_to: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c.RUN_AUTO_BOT, callback_data=c.CD_RUN_AUTO_BOT)],
            [go_back_btn(go_to)],
        ]
    )


def get_purchase_subscription(product_id: int, subscription_price: int, go_back: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=t.buy_subscription_btn_text(subscription_price),
                callback_data=Subscription(product_id=product_id).pack())],
            [go_back_btn(go_back)],
        ]
    )


def get_info(go_to: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c.SUPPORT, url=settings.SUPPORT_LINK)],
            [InlineKeyboardButton(text=c.OFFICIAL_CHANNEL, url=settings.OFFICIAL_CHANNEL_LINK)],
            [InlineKeyboardButton(text=c.OFFICIAL_CHAT, url=settings.OFFICIAL_CHAT_LINK)],
            [go_back_btn(go_to)],
        ]
    )
