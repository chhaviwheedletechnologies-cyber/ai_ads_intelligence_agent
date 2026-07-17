from datetime import datetime

from database.mongo import mongo

from services.google_ads_service import GoogleAdsService


class ExecutionService:

    def __init__(self):

        self.google_ads = GoogleAdsService()

        self.collection = mongo.get_collection("execution_logs")

    ##########################################################

    def execute(self, campaign_id, ai_decision):

        executed_actions = []

        ##################################################

        decision = ai_decision.get("decision", "").lower()

        ##################################################

        if decision == "pause":

            result = self.google_ads.pause_campaign(campaign_id)

            executed_actions.append(result)

        ##################################################

        if ai_decision.get("budget_action") == "increase":

            result = self.google_ads.update_campaign_budget(

                campaign_id,

                ai_decision.get("recommended_budget")

            )

            executed_actions.append(result)

        ##################################################

        if ai_decision.get("budget_action") == "reduce":

            result = self.google_ads.update_campaign_budget(

                campaign_id,

                ai_decision.get("recommended_budget")

            )

            executed_actions.append(result)

        ##################################################

        negative_keywords = ai_decision.get("negative_keywords", [])

        if negative_keywords:

            result = self.google_ads.add_negative_keywords(

                campaign_id,

                negative_keywords

            )

            executed_actions.append(result)

        ##################################################

        bid = ai_decision.get("recommended_bid")

        if bid is not None:

            result = self.google_ads.update_keyword_bids(

                campaign_id,

                bid

            )

            executed_actions.append(result)

        ##################################################

        if ai_decision.get("resume_campaign"):

            result = self.google_ads.enable_campaign(campaign_id)

            executed_actions.append(result)

        ##################################################

        log = {

            "campaign_id": campaign_id,

            "decision": ai_decision,

            "actions": executed_actions,

            "executed_at": datetime.utcnow()

        }

        self.collection.insert_one(log)

        ##################################################

        return {

            "status": "success",

            "campaign_id": campaign_id,

            "actions": executed_actions

        }