from src.config.settings import settings
from src.config import logger
# from src.webhooks.cryptobot import handle_payment as handle_crypto


def setup_routes(app):
    ...
    # app.router.add_post(settings.crypto_bot_webhook_endpoint, handle_crypto)


def setup_callbacks(app):
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


async def on_startup(app):
    logger.debug("[Webhook API Server] - starting up")


async def on_shutdown(app):
    logger.debug("[Webhook API Server] - shutting down")
