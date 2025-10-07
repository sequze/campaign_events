from pydantic import BaseModel, PositiveInt
from core.models.event import StatusEnum


class SEventModel(BaseModel):
    account_id: PositiveInt
    chat_id: PositiveInt
    message_id: PositiveInt
    status: StatusEnum
    campaign_id: PositiveInt


class EventDTO(SEventModel):
    id: PositiveInt

    class Config:
        from_attributes = True
