from aiohttp import web

from src.config import settings, logger
from src.loader import db_helper
from src.repositories import SqlAlchemyHamsterCodeRepository


async def handle_keys(request):
    logger.info('Get new keys from gateway!')
    result = await request.json()
    secret_key = result.get('secret_key')
    if secret_key != settings.GATEWAY_KEYS_SECRET:
        return web.Response(status=403)

    keys = result.get('data', {})
    await add_keys(keys)
    return web.Response(status=200)


async def add_keys(keys: dict):
    try:
        async with db_helper.get_db() as session:
            hamster_repo = SqlAlchemyHamsterCodeRepository(session)
            for game_id in keys:
                try:
                    await hamster_repo.add_codes(
                        codes={game_id: keys[game_id]}
                    )
                    logger.info(f'Keys for game_id: {game_id} successfully added!')
                except Exception as ex:
                    logger.error(f'error add_codes for game_id: {game_id}|: {ex}')
    except Exception as ex:
        logger.error(f'gateway keys: {ex}')
