from datetime import datetime

from database.mongo import mongo


class NotificationService:

    def __init__(self):

        self.collection = mongo.get_collection("notifications")

    ##########################################################

    def send_notification(

        self,

        campaign_id,

        title,

        message,

        notification_type="info"

    ):

        notification = {

            "campaign_id": campaign_id,

            "title": title,

            "message": message,

            "type": notification_type,

            "status": "sent",

            "created_at": datetime.utcnow()

        }

        self.collection.insert_one(notification)

        return {

            "status": "success",

            "notification": notification

        }

    ##########################################################

    def campaign_paused(self, campaign_id):

        return self.send_notification(

            campaign_id,

            "Campaign Paused",

            "Campaign has been paused automatically by AI.",

            "warning"

        )

    ##########################################################

    def campaign_enabled(self, campaign_id):

        return self.send_notification(

            campaign_id,

            "Campaign Enabled",

            "Campaign has been enabled after AI optimization.",

            "success"

        )

    ##########################################################

    def budget_updated(

        self,

        campaign_id,

        budget

    ):

        return self.send_notification(

            campaign_id,

            "Budget Updated",

            f"Budget updated to ₹{budget}.",

            "info"

        )

    ##########################################################

    def negative_keywords_added(

        self,

        campaign_id,

        keywords

    ):

        return self.send_notification(

            campaign_id,

            "Negative Keywords Added",

            f"Added keywords: {', '.join(keywords)}",

            "info"

        )

    ##########################################################

    def report_generated(

        self,

        campaign_id

    ):

        return self.send_notification(

            campaign_id,

            "AI Report Generated",

            "Daily AI report is ready.",

            "success"

        )

    ##########################################################

    def ai_recommendation(

        self,

        campaign_id,

        recommendation

    ):

        return self.send_notification(

            campaign_id,

            "AI Recommendation",

            recommendation,

            "info"

        )