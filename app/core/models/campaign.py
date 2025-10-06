from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .event import Event


class Campaign(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    events: Mapped[list["Event"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
