from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import logger
from src.database.models import HamsterCode
from .base import IHamsterCodeRepository


class SqlAlchemyHamsterCodeRepository(IHamsterCodeRepository):
    model = HamsterCode

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_code(self, game_id: int, code: str):
        try:
            new_code = HamsterCode(game_id=game_id, code=code)
            self.session.add(new_code)
            await self.session.commit()
            logger.debug(f"Code '{code}' added for game_id '{game_id}'.")
        except Exception as ex:
            await self.session.rollback()
            logger.error(f"Error adding code '{code}' for game_id '{game_id}': {ex}")

    async def add_codes(self, codes: dict[int, list]):
        try:
            new_codes = []
            for game_id in codes:
                new_codes.extend([HamsterCode(game_id=int(game_id), code=code) for code in codes[game_id]])

            self.session.add_all(new_codes)
            await self.session.commit()
            logger.debug(f"Added {len(new_codes)}")
        except IntegrityError as ex:
            await self.session.rollback()
            logger.error(f"Integrity error while adding codes: {ex}")
            raise
        except Exception as ex:
            await self.session.rollback()
            logger.error(f"Error adding codes: {ex}")

    async def get_code(self, game_id: int) -> HamsterCode | None:
        try:
            result = await self.session.execute(
                select(self.model).filter_by(game_id=game_id, is_used=False).order_by(self.model.id)
            )
            code = result.scalars().first()
            if code:
                await self.set_is_used(code.id, is_used=True)
                logger.debug(f"Code '{code.code}' retrieved for game_id '{game_id}'.")
            else:
                logger.debug(f"No available codes found for game_id '{game_id}'.")
            return code
        except Exception as ex:
            logger.error(f"Error retrieving code for game_id '{game_id}': {ex}")

    async def get_codes(self, game_id: int, code_count: int) -> list[HamsterCode]:
        try:
            result = await self.session.execute(
                select(self.model)
                .filter_by(game_id=game_id, is_used=False)
                .order_by(self.model.id)
                .limit(code_count)
            )
            codes = result.scalars().all()

            if codes:
                code_ids = [code.id for code in codes]
                await self.set_is_used(code_ids, is_used=True)
                logger.debug(f"Retrieved and marked {len(codes)} codes as used for game_id '{game_id}'.")
            else:
                logger.debug(f"No available codes found for game_id '{game_id}'.")

            return list(codes)

        except Exception as ex:
            await self.session.rollback()
            logger.error(f"Error retrieving and updating codes for game_id '{game_id}': {ex}")
            return []

    async def set_is_used(self, code_ids: int | list, is_used: bool = True):
        if isinstance(code_ids, int):
            code_ids = [code_ids]

        try:
            stmt = (
                update(self.model)
                .where(self.model.id.in_(code_ids))
                .values(is_used=is_used)
            )
            await self.session.execute(stmt)
            await self.session.commit()
            logger.debug(f"Code with ids '{code_ids}' set to is_used='{is_used}'.")
        except Exception as ex:
            await self.session.rollback()
            logger.error(f"Error setting code with id '{code_ids}' to is_used='{is_used}': {ex}")
            raise

    async def count_unused_codes(self, game_id: int) -> int:
        try:
            result = await self.session.execute(
                select(func.count()).select_from(self.model).filter_by(game_id=game_id, is_used=False)
            )
            count = result.scalar()
            return count
        except Exception as ex:
            logger.error(f"Error counting unused codes for game_id '{game_id}': {ex}")
            return 0
