from fastapi import APIRouter

from services.google_ads_service import GoogleAdsService

router = APIRouter(
    prefix="/campaign",
    tags=["Campaign"]
)

service = GoogleAdsService()


@router.get("/list")
def list_campaigns():

    return service.list_campaigns()


@router.get("/{campaign_id}")
def get_campaign(campaign_id: int):

    campaign = service.get_campaign(campaign_id)

    if campaign is None:

        return {

            "status": "failed",

            "message": "Campaign not found."

        }

    return campaign