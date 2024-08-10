from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import Base


class HamsterCode(Base):
    game_id: Mapped[int] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    is_used: Mapped[bool] = mapped_column(default=False)
