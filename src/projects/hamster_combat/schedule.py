import asyncio

from src.config import logger
from src.loader import db_helper
from src.projects.hamster_combat.game_codes_generator import GameRepository, PromoCodeGenerator
from src.repositories import SqlAlchemyHamsterCodeRepository


async def promo_generation(hamster_repo, game_id, generate_count):
    generator = PromoCodeGenerator(game_id)
    promo_codes = await generator.generate_promo_codes(generate_count)

    await hamster_repo.add_codes(
        codes={game_id: promo_codes}
    )


async def hamster_codes_filling_if_necessary(min_codes_count: int):
    async with db_helper.get_db() as session:
        hamster_repo = SqlAlchemyHamsterCodeRepository(session)
        tasks = []

        for game_id in GameRepository.games.keys():
            count = await hamster_repo.count_unused_codes(game_id=int(game_id))
            if min_codes_count > count:

                logger.info(f'Не хватает {min_codes_count-count} кодов для game_id: {game_id}')
                tasks.append(asyncio.create_task(promo_generation(hamster_repo, game_id, min_codes_count-count + 10)))

        await asyncio.gather(*tasks)


