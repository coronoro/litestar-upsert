from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from sqlalchemy import types


class Card(UUIDAuditBase):
    __tablename__ = "cards"

    name: Mapped[str]
    external_id: Mapped[str] = mapped_column(types.String, unique=True)

