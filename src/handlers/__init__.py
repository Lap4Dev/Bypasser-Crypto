from aiogram import Router


def register_routers() -> Router:
    router = Router()

    from .users import register_routers
    from .admins import register_routers as admins_register_routers
    from .default import router as default_router
    router.include_routers(
        register_routers(),
        admins_register_routers(),
        default_router
    )
    return router
