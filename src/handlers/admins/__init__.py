from aiogram import Router


def register_routers() -> Router:
    router = Router()

    from .notifications import router as notifications_router

    router.include_routers(
        notifications_router,
    )
    return router

