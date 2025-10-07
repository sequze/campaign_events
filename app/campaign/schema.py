from pydantic import BaseModel, PositiveInt


class SCampaignModel(BaseModel):
    name: str


class CampaignDTO(SCampaignModel):
    id: PositiveInt

    class Config:
        from_attributes = True
