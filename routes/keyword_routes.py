from fastapi import APIRouter

from services.google_ads_service import GoogleAdsService
from services.keyword_optimizer import KeywordOptimizer

router = APIRouter(
    prefix="/keywords",
    tags=["Keyword Optimization"]
)

google_ads = GoogleAdsService()
keyword_optimizer = KeywordOptimizer()


########################################################


@router.get("/{campaign_id}")
def get_keywords(campaign_id: int):

    return google_ads.get_keywords(campaign_id)


########################################################


@router.get("/{campaign_id}/search-terms")
def get_search_terms(campaign_id: int):

    return google_ads.get_search_terms(campaign_id)


########################################################


@router.post("/{campaign_id}/optimize")
def optimize_keywords(campaign_id: int):

    return keyword_optimizer.optimize_keywords(campaign_id)