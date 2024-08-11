from aiogram.filters.callback_data import CallbackData


class HamsterGame(CallbackData, prefix='hmstr-code'):
    game_id: int


class Subscription(CallbackData, prefix='buy-subs'):
    product_id: int
