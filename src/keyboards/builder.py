from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.callback_data import HamsterGame
from src.config.constants import CHECK_SUBSCRIPTION, HAMSTER_GAMES, GO_BACK
from src.schemas import PartnerChannelSchema


def get_partner(channels: list[PartnerChannelSchema]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    [builder.button(text=channel.name, url=channel.channel_link) for channel in channels]
    builder.button(text=CHECK_SUBSCRIPTION, callback_data=CHECK_SUBSCRIPTION)
    builder.adjust(1)
    return builder.as_markup()


def get_hamster_games(go_back_to: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    [builder.button(text=game[1], callback_data=HamsterGame(game_id=game[0]).pack()) for game in HAMSTER_GAMES]
    builder.button(text=GO_BACK, callback_data=go_back_to)
    builder.adjust(2)
    return builder.as_markup()
