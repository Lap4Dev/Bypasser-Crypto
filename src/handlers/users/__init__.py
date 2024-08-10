from aiogram import Router


def register_routers() -> Router:
    router = Router()

    from .commands import router as commands_router
    from .hamster_combat import router as hamster_combat_router
    from .referral_program import router as referral_program_router
    router.include_routers(
        commands_router,
        hamster_combat_router,
        referral_program_router
    )
    return router

