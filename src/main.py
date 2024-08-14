import os
import sys
from contextlib import suppress

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.loader import dp, bot

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.schedule_tasks import setup_schedule_tasks
from src.config import settings, logger


async def setup_middlewares_and_routers():
    from src.middlewares import setup_middlewares
    from src.handlers import register_routers

    await setup_middlewares(dp)
    dp.include_routers(register_routers())


async def on_startup():
    from src.utils.bot_commands import set_commands
    await set_commands(bot)

    await setup_middlewares_and_routers()

    await bot.set_webhook(settings.TELEGRAM_WEBHOOK_URL,
                          secret_token=settings.WEBHOOK_SECRET,
                          drop_pending_updates=True)

    logger.info('Bot successfully started!')


async def on_shutdown():
    logger.info('Bot shutdown!')


def setup_bot_webhooks(app: web.Application):
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)


def setup_web_app() -> web.Application:
    from src.webhooks import setup_routes, setup_callbacks

    app = web.Application()
    setup_routes(app)
    setup_callbacks(app)
    return app


def main():
    dp.startup.register(on_startup)

    app = setup_web_app()
    setup_bot_webhooks(app)
    setup_application(app, dp, bot=bot)

    scheduler = AsyncIOScheduler()
    setup_schedule_tasks(scheduler, bot)
    scheduler.start()

    web.run_app(app, host=settings.WEB_SERVER_HOST, port=settings.WEB_SERVER_PORT)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt, SystemExit):
        main()

# async def main():
# bot = Bot(
#     token=settings.BOT_TOKEN.get_secret_value(),
#     default=DefaultBotProperties(parse_mode=ParseMode.HTML)
# )
# from src.utils.bot_commands import set_commands
# await set_commands(bot)
#
# dp = Dispatcher()

# from src.middlewares import setup_middlewares
# await setup_middlewares(dp)

# from src.handlers import register_routers
# dp.include_routers(register_routers())

# await bot.delete_webhook(drop_pending_updates=True)
#
# scheduler = AsyncIOScheduler()
# setup_schedule_tasks(scheduler, bot)
# scheduler.start()
#
# await dp.start_polling(bot)
