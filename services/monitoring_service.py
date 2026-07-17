from datetime import datetime

from database.mongo import mongo
from services.google_ads_service import GoogleAdsService


class MonitoringService:

    def __init__(self):

        self.google_ads = GoogleAdsService()

        self.collection = mongo.get_collection("monitoring_logs")

    ########################################################

    def monitor_campaign(self, request):

        campaign_id = request.campaign_id

        metrics = self.google_ads.get_campaign_metrics(campaign_id)

        if metrics is None:

            return {

                "status": "failed",

                "message": "Campaign not found."

            }

        monitoring_data = {

            "campaign_id": metrics["campaign_id"],

            "campaign_name": metrics["campaign_name"],

            "impressions": metrics["impressions"],

            "clicks": metrics["clicks"],

            "ctr": metrics["ctr"],

            "average_cpc": metrics["average_cpc"],

            "cost": metrics["cost"],

            "conversions": metrics["conversions"],

            "monitored_at": datetime.utcnow()

        }

        self.collection.insert_one(monitoring_data)
        
        monitoring_data["_id"] = str(monitoring_data["_id"])

        return {

            "status": "success",

            "message": "Campaign monitored successfully.",

            "data": monitoring_data

        }