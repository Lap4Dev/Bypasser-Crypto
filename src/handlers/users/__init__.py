from aiogram import Router


def register_routers() -> Router:
    router = Router()

    from .commands import router as commands_router
    from .hamster_combat_keys import router as hamster_combat__keys_router
    from .hamster_kombat_claimer import router as hamster_combat__claimer_router
    from .referral_program import router as referral_program_router
    from .subscription import router as subscription_router
    router.include_routers(
        commands_router,
        hamster_combat__keys_router,
        hamster_combat__claimer_router,
        referral_program_router,
        subscription_router
    )
    return router

