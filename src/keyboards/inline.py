from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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


def go_menu_btn() -> InlineKeyboardButton:
    return InlineKeyboardButton(text=c.MENU, callback_data=c.CD_MAIN_MENU)


def go_back_to(go_to: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [go_back_btn(go_to)],
        ]
    )


def get_close():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c.CLOSE, callback_data=c.CD_CLOSE)],
        ]
    )


def get_url_kb(text, url):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=url)],
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


def get_purchase_subscription(subscription_price: int, payment_url: str, go_back: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=t.buy_subscription_btn_text(subscription_price),
                # callback_data=Subscription(product_id=product_id).pack())],
                url=payment_url
            )],
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


def get_support():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c.SUPPORT, url=settings.SUPPORT_LINK)],
            [InlineKeyboardButton(text=c.MENU, callback_data=c.CD_MAIN_MENU)],
        ]
    )


def get_claimer_menu(is_claimer_run: bool, is_empty_token: bool, go_to: str):
    keyboard = []

    if is_empty_token:
        keyboard.append([InlineKeyboardButton(text=c.SET_TOKEN, callback_data=c.CD_SET_TOKEN)])
    else:
        if is_claimer_run:
            keyboard.append([InlineKeyboardButton(text=c.STOP_CLAIMER, callback_data=c.CD_STOP_CLAIMER)])
        else:
            keyboard.append([InlineKeyboardButton(text=c.RUN_CLAIMER, callback_data=c.CD_RUN_CLAIMER)])

        keyboard.append([InlineKeyboardButton(text=c.CHANGE_TOKEN, callback_data=c.CD_CHANGE_TOKEN)])

    keyboard.append([go_back_btn(go_to), ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cancel(go_to: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c.CANCEL, callback_data=go_to)],
        ]
    )


def mailing_confirm():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=c.CONFIRM_SENDING, callback_data=c.CD_CONFIRM_SENDING)],
        [InlineKeyboardButton(text=c.CANCEL, callback_data=c.CD_CLOSE)],
    ])
