from datetime import datetime
from pymongo.errors import DuplicateKeyError

from database.mongo import mongo
from services.google_ads_service import GoogleAdsService
from services.budget_optimizer import BudgetOptimizer
from services.keyword_optimizer import KeywordOptimizer
from services.report_service import ReportService
from services.campaign_auto_fixer import CampaignAutoFixer
from services.openai_service import OpenAIService


class AgentOrchestrator:

    def __init__(self):

        self.agent_logs_collection = mongo.get_collection("agent_optimization_logs")
        self.agent_logs_collection.create_index("campaign_id", unique=True)

        self.google_ads = GoogleAdsService()
        self.budget_optimizer = BudgetOptimizer()
        self.keyword_optimizer = KeywordOptimizer()
        self.report_service = ReportService()
        self.auto_fixer = CampaignAutoFixer()
        self.ai = OpenAIService()

    ##########################################################

    def process_active_campaigns(self):

        all_campaigns = self.google_ads.list_campaigns()

        active_campaigns = [
            c for c in all_campaigns if c["status"] == "ENABLED"
        ]

        processed_count = 0
        skipped_count = 0
        processed_results = []

        for campaign in active_campaigns:

            campaign_id = campaign["campaign_id"]

            already_done = self.agent_logs_collection.find_one(
                {"campaign_id": campaign_id}
            )

            if already_done:
                skipped_count += 1
                continue

            ##################################################
            # Fetch metrics, keywords, search terms
            ##################################################

            metrics = self.google_ads.get_campaign_metrics(campaign_id)
            search_terms = self.google_ads.get_search_terms(campaign_id)

            budget_recommendation = (
                self.budget_optimizer.optimize_budget(metrics)
                if metrics else None
            )

            keyword_recommendation = self.keyword_optimizer.optimize_keywords(
                campaign_id
            )

            report = self.report_service.generate_report(campaign_id)

            ##################################################
            # Error detection + auto-fix (dry-run mode)
            ##################################################

            fix_result = self.auto_fixer.run(campaign_id, metrics, search_terms)

            ##################################################
            # AI-generated client report
            ##################################################

            ai_client_report = self.ai.generate_client_report({
                "campaign_name": campaign["campaign_name"],
                "metrics": metrics,
                "budget_recommendation": budget_recommendation,
                "keyword_recommendation": keyword_recommendation,
                "errors_found": fix_result["errors_found"],
                "actions_taken": fix_result["actions_taken"],
            })

            now = datetime.utcnow()

            ##################################################
            # Final document
            ##################################################

            result = {
                "campaign_id": campaign_id,
                "campaign_name": campaign["campaign_name"],
                "platform": "google",
                "status": campaign["status"],

                "campaign_activated_at": now,
                "optimized_at": now,
                "updated_at": now,

                "metrics": metrics,
                "budget_recommendation": budget_recommendation,
                "keyword_recommendation": keyword_recommendation,
                "report": report,

                "errors_found": fix_result["errors_found"],
                "actions_taken": fix_result["actions_taken"],
                "dry_run": fix_result["dry_run"],

                "ai_client_report": ai_client_report,
            }

            try:
                self.agent_logs_collection.insert_one(result)
                processed_count += 1

                result["_id"] = str(result["_id"])
                processed_results.append(result)

                print(f"[Agent] Optimized campaign {campaign_id} ({campaign['campaign_name']})")

            except DuplicateKeyError:
                skipped_count += 1

        print(
            f"[Agent] Run complete. "
            f"{processed_count} new campaign(s) optimized, "
            f"{skipped_count} already processed (skipped)."
        )

        return {
            "processed": processed_count,
            "skipped": skipped_count,
            "results": processed_results
        }