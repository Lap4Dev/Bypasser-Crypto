from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.callback_data import Subscription

router = Router()


@router.callback_query(Subscription.filter())
async def handle_subscription_purchase(query: CallbackQuery, callback_data: Subscription):
    product_id = callback_data.product_id
