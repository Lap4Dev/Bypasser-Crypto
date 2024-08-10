from abc import ABC, abstractmethod


class IHamsterCodeRepository(ABC):
    model = None

    @abstractmethod
    async def add_code(self, game_id: int, code: str):
        ...

    @abstractmethod
    async def get_codes(self, game_id: int, code_count: int):
        ...

    @abstractmethod
    async def get_code(self, game_id: int):
        ...

    @abstractmethod
    async def set_is_used(self, code_id: int, is_used: bool = True):
        ...

    @abstractmethod
    async def count_unused_codes(self, game_id: int) -> int:
        ...
