from datetime import datetime

from services.google_ads_service import GoogleAdsService
from services.error_detector import ErrorDetector
from services.openai_service import OpenAIService

# DRY_RUN = True means no real changes happen on Google Ads.
# Everything is detected and logged, but pause/fix/enable actions
# are only simulated. Set to False later when ready to go live.
DRY_RUN = True


class CampaignAutoFixer:

    def __init__(self):
        self.google_ads = GoogleAdsService()
        self.error_detector = ErrorDetector()
        self.ai = OpenAIService()

    ##########################################################

    def run(self, campaign_id, metrics, search_terms):

        actions_taken = []

        ##################################################
        # Step 1: Detect errors
        ##################################################

        performance_errors = self.error_detector.detect_performance_errors(metrics)

        try:
            policy_issues = self.google_ads.get_policy_issues(campaign_id)
        except Exception as e:
            policy_issues = []
            print(f"[AutoFixer] Could not fetch policy issues: {e}")

        policy_errors = self.error_detector.detect_policy_errors(policy_issues)

        all_errors = performance_errors + policy_errors

        if not all_errors:
            return {
                "errors_found": [],
                "actions_taken": [],
                "dry_run": DRY_RUN
            }

        ##################################################
        # Step 2: Pause campaign
        ##################################################

        if DRY_RUN:
            actions_taken.append({
                "action": "pause_campaign",
                "status": "simulated",
                "detail": "Dry-run mode: campaign would be paused here."
            })
        else:
            pause_result = self.google_ads.pause_campaign(campaign_id)
            actions_taken.append({"action": "pause_campaign", "result": pause_result})

        ##################################################
        # Step 3: AI-suggested negative keyword fix
        ##################################################

        negative_suggestions = self.ai.suggest_negative_keywords(search_terms)

        if negative_suggestions:

            if DRY_RUN:
                actions_taken.append({
                    "action": "add_negative_keywords",
                    "status": "simulated",
                    "suggestions": negative_suggestions
                })
            else:
                keywords = [s["keyword"] for s in negative_suggestions]
                result = self.google_ads.add_negative_keywords(campaign_id, keywords)
                actions_taken.append({
                    "action": "add_negative_keywords",
                    "result": result,
                    "suggestions": negative_suggestions
                })

        ##################################################
        # Step 4: Re-enable campaign
        ##################################################

        if DRY_RUN:
            actions_taken.append({
                "action": "enable_campaign",
                "status": "simulated",
                "detail": "Dry-run mode: campaign would be re-enabled here."
            })
        else:
            enable_result = self.google_ads.enable_campaign(campaign_id)
            actions_taken.append({"action": "enable_campaign", "result": enable_result})

        return {
            "errors_found": all_errors,
            "actions_taken": actions_taken,
            "dry_run": DRY_RUN,
            "processed_at": datetime.utcnow()
        }