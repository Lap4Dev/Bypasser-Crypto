from abc import ABC, abstractmethod

from src.database.models import Product


class IProductRepository(ABC):
    model = None

    @abstractmethod
    async def get_by_name(self, product_name: str) -> Product | None:
        ...


