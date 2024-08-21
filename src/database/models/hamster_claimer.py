from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import Base


class HamsterClaimer(Base):
    user_id: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    token_id: Mapped[int] = mapped_column(nullable=True, default=None)
    
