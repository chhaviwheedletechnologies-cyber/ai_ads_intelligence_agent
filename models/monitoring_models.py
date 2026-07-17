from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MonitoringRequest(BaseModel):

    campaign_id: str


class CampaignMetrics(BaseModel):

    campaign_id: str

    campaign_name: Optional[str] = None

    impressions: int

    clicks: int

    ctr: float

    average_cpc: float

    cost: float

    conversions: float

    conversion_rate: float

    cpa: float

    roas: float

    quality_score: Optional[float] = None

    status: Optional[str] = None

    monitored_at: datetime


class MonitoringResponse(BaseModel):

    status: str

    message: str

    metrics: CampaignMetrics