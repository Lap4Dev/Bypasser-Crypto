import json

from aiocryptopay.const import InvoiceStatus
from aiocryptopay.models.update import Update
from aiohttp import web

from src.config import logger
from src.loader import db_helper
from src.schemas import PaymentPayload
from src.services.subscription_service import SubscriptionService
from src.utils.bot import send_message_after_success_subscription


async def handle_payment(request):
    update = await request.json()
    await verify_invoice(Update(**update))
    return web.Response(status=200)


async def verify_invoice(update: Update):
    print(update)
    logger.info(f'Received new crypto_bot webhook: {update}')
    payload = update.payload
    if payload.status == InvoiceStatus.PAID:
        async with db_helper.get_db() as session:
            subs_service = SubscriptionService(session)

            try:
                payment_payload = json.loads(payload.payload)
                payment_payload['invoice_id'] = str(payload.invoice_id)
                payment_payload['payment_service'] = 'CRYPTO_BOT'

                payment_payload = PaymentPayload(**payment_payload)
            except Exception as ex:
                logger.error(f'Error while parsing CRYPTO_BOT payload: [{payload.payload}]: {ex}')
                return

            subscription = await subs_service.confirm_payment(payment_payload)

            if not subscription:
                logger.error(f'Error while confirming payment with payload: [ {payment_payload} ]')
                return

            await send_message_after_success_subscription(
                user_id=payment_payload.user_id,
                product_name=payment_payload.product_name,
                subscription=subscription,
                session=session
            )
