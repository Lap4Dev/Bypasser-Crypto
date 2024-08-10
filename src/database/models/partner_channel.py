from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base_model import Base


class PartnerChannel(Base):
    channel_link: Mapped[str] = mapped_column(String(255), nullable=False)
    channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
