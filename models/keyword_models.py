from pydantic import BaseModel
from typing import List
from datetime import datetime


class KeywordOptimizationRequest(BaseModel):

    campaign_id: str

    keywords: List[str]

    search_terms: List[str]


class KeywordRecommendation(BaseModel):

    campaign_id: str

    suggested_keywords: List[str]

    negative_keywords: List[str]

    removed_keywords: List[str]

    ai_summary: str

    created_at: datetime