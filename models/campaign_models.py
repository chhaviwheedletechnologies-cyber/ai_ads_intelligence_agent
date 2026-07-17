from pydantic import BaseModel
from typing import Optional


class CampaignRequest(BaseModel):

    campaign_id: Optional[str] = None

    campaign_name: str

    budget: float

    objective: str

    target_location: str

    language: str

    bidding_strategy: str

    daily_budget: float


class CampaignResponse(BaseModel):

    status: str

    message: str

    campaign_id: Optional[str]