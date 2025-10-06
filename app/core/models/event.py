from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .campaign import Campaign


class StatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Event(Base, IntIdPkMixin):
    account_id: Mapped[int] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    message_id: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        default=StatusEnum.PENDING,
        nullable=False,
    )
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
    )

    campaign: Mapped["Campaign"] = relationship(back_populates="events")

    __table_args__ = (UniqueConstraint("campaign_id", "chat_id", "message_id"),)

    def __str__(self):
        return f"Event {self.id}"
