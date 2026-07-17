from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BudgetOptimizationRequest(BaseModel):

    campaign_id: str

    current_budget: float

    current_spend: float

    current_roas: float

    current_cpa: float


class BudgetRecommendation(BaseModel):

    campaign_id: str

    current_budget: float

    recommended_budget: float

    budget_change_percent: float

    reason: str

    ai_summary: Optional[str] = None

    created_at: datetime