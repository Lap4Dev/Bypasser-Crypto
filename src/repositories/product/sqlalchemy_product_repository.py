from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Product
from .base import IProductRepository


class SqlAlchemyProductRepository(IProductRepository):
    model: Product = Product

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_by_name(self, product_name: str) -> Product | None:
        result = await self.session.execute(
            select(self.model).where(
                self.model.name == product_name
            )
        )
        return result.scalars().first()

