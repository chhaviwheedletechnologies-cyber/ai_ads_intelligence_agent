from google.ads.googleads.client import GoogleAdsClient
from config.settings import settings
from database.mongo import mongo
import datetime


class GoogleAdsService:

    def __init__(self):
        google_ads_config = {
            "developer_token": settings.GOOGLE_ADS_DEVELOPER_TOKEN,
            "client_id": settings.GOOGLE_ADS_CLIENT_ID,
            "client_secret": settings.GOOGLE_ADS_CLIENT_SECRET,
            "refresh_token": settings.GOOGLE_ADS_REFRESH_TOKEN,
            "login_customer_id": settings.GOOGLE_ADS_LOGIN_CUSTOMER_ID,
            "use_proto_plus": True,
        }

        self.client = GoogleAdsClient.load_from_dict(google_ads_config)
        self.customer_id = settings.GOOGLE_ADS_CUSTOMER_ID
        self.collection = mongo.get_collection("campaigns")

    # ------------------------------------------------------------------

    def get_client(self):
        return self.client

    # ------------------------------------------------------------------

    def list_campaigns(self):
        ga_service = self.client.get_service("GoogleAdsService")

        query = """
        SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        campaign.advertising_channel_type
        FROM campaign
        """

        response = ga_service.search(
            customer_id=self.customer_id,
            query=query
        )

        campaigns = []

        for row in response:
            campaigns.append({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "status": row.campaign.status.name,
                "channel": row.campaign.advertising_channel_type.name
            })

        return campaigns

    # ------------------------------------------------------------------

    def get_campaign(self, campaign_id):
        ga_service = self.client.get_service("GoogleAdsService")

        query = f"""
        SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        campaign.advertising_channel_type
        FROM campaign
        WHERE campaign.id = {campaign_id}
        """

        response = ga_service.search(
            customer_id=self.customer_id,
            query=query
        )

        for row in response:
            return {
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "status": row.campaign.status.name,
                "channel": row.campaign.advertising_channel_type.name
            }

        return None

    # ------------------------------------------------------------------

    def get_campaign_metrics(self, campaign_id):
        ga_service = self.client.get_service("GoogleAdsService")

        query = f"""
        SELECT
            campaign.id,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE campaign.id = {campaign_id}
        """

        response = ga_service.search(
            customer_id=self.customer_id,
            query=query
        )

        for row in response:
            impressions = row.metrics.impressions
            clicks = row.metrics.clicks
            conversions = row.metrics.conversions
            conversions_value = row.metrics.conversions_value
            cost = row.metrics.cost_micros / 1000000

            amount_spent = cost
            average_cpm = (cost / impressions * 1000) if impressions else 0
            conversion_rate = (conversions / clicks * 100) if clicks else 0
            cpa = (cost / conversions) if conversions else 0
            roas = (conversions_value / cost) if cost else 0

            return {
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "impressions": impressions,
                "clicks": clicks,
                "ctr": row.metrics.ctr,
                "average_cpc": row.metrics.average_cpc,
                "cost": cost,
                "conversions": conversions,
                "amount_spent": amount_spent,
                "average_cpm": average_cpm,
                "conversion_rate": conversion_rate,
                "cpa": cpa,
                "roas": roas
            }

        return None

    # ------------------------------------------------------------------

    def create_campaign(self, request):
        data = request.model_dump()
        data["created_at"] = datetime.datetime.utcnow()

        self.collection.insert_one(data)

        return {
            "status": "success",
            "message": "Campaign request stored successfully.",
            "campaign": data
        }

    # ------------------------------------------------------------------

    def pause_campaign(self, campaign_id):
        return {
            "status": "pending",
            "message": f"Pause Campaign {campaign_id} (Google Ads API mutation will be implemented in Execution Service)."
        }

    # ------------------------------------------------------------------

    def update_campaign_budget(self, campaign_id, budget):
        return {
            "status": "pending",
            "campaign_id": campaign_id,
            "new_budget": budget,
            "message": "Budget update will be executed through Google Ads API."
        }

    # ------------------------------------------------------------------

    def add_negative_keywords(self, campaign_id, keywords):
        return {
            "status": "pending",
            "campaign_id": campaign_id,
            "negative_keywords": keywords,
            "message": "Negative keywords will be added through Google Ads API."
        }

    # ------------------------------------------------------------------

    def update_keyword_bids(self, campaign_id, bid):
        return {
            "status": "pending",
            "campaign_id": campaign_id,
            "new_bid": bid,
            "message": "Keyword bid update will be executed through Google Ads API."
        }

    # ------------------------------------------------------------------

    def get_search_terms(self, campaign_id):
        ga_service = self.client.get_service("GoogleAdsService")

        query = f"""
        SELECT
        search_term_view.search_term,
        metrics.clicks,
        metrics.impressions,
        metrics.conversions
        FROM search_term_view
        WHERE campaign.id = {campaign_id}
        """

        response = ga_service.search(
            customer_id=self.customer_id,
            query=query
        )

        terms = []

        for row in response:
            terms.append({
                "search_term": row.search_term_view.search_term,
                "clicks": row.metrics.clicks,
                "impressions": row.metrics.impressions,
                "conversions": row.metrics.conversions
            })

        return terms

    # ------------------------------------------------------------------

    def get_keywords(self, campaign_id):
        ga_service = self.client.get_service("GoogleAdsService")

        query = f"""
        SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.status,
        metrics.clicks,
        metrics.impressions,
        metrics.conversions
        FROM keyword_view
        WHERE campaign.id = {campaign_id}
        """

        response = ga_service.search(
            customer_id=self.customer_id,
            query=query
        )

        keywords = []

        for row in response:
            keywords.append({
                "keyword": row.ad_group_criterion.keyword.text,
                "status": row.ad_group_criterion.status.name,
                "clicks": row.metrics.clicks,
                "impressions": row.metrics.impressions,
                "conversions": row.metrics.conversions
            })

        return keywords

    # ------------------------------------------------------------------

    def enable_campaign(self, campaign_id):
        return {
            "status": "pending",
            "message": f"Enable Campaign {campaign_id} (Google Ads API mutation will be implemented in Execution Service)."
        }