from apscheduler.schedulers.background import BackgroundScheduler

from services.google_ads_service import GoogleAdsService
from services.monitoring_service import MonitoringService
from services.rule_engine import RuleEngine
from services.ai_analysis_service import AIAnalysisService
from services.execution_service import ExecutionService
from services.notification_service import NotificationService


class MonitoringScheduler:

    def __init__(self):

        self.google_ads = GoogleAdsService()

        self.monitoring = MonitoringService()

        self.rule_engine = RuleEngine()

        self.ai_analysis = AIAnalysisService()

        self.execution = ExecutionService()

        self.notification = NotificationService()

        self.scheduler = BackgroundScheduler()

    ############################################################

    def monitor_campaigns(self):

        print("Starting AI Campaign Monitoring...")

        campaigns = self.google_ads.list_campaigns()

        for campaign in campaigns:

            campaign_id = campaign["campaign_id"]

            try:

                ##################################################

                metrics = self.google_ads.get_campaign_metrics(
                    campaign_id
                )

                ##################################################

                monitoring_data = self.monitoring.save_metrics(
                    campaign_id,
                    metrics
                )

                ##################################################

                rule_result = self.rule_engine.evaluate(metrics)
                 
                ##################################################

                if rule_result["status"] == "healthy":

                    continue

                ##################################################

                ai_result = self.ai_analysis.analyze_campaign({
                  "metrics": metrics,

                  "rules": rule_result
                })

                ##################################################

                execution = self.execution.execute(

                    campaign_id,

                    ai_result

                )

                ##################################################

                self.notification.ai_recommendation(

                    campaign_id,

                    ai_result.get("summary", "AI Optimization Applied")

                )

                ##################################################

                print(execution)

            except Exception as e:

                print(

                    f"Monitoring Error ({campaign_id}) : {e}"

                )

    ############################################################

    def start(self):

        self.scheduler.add_job(

            self.monitor_campaigns,

            trigger="interval",

            minutes=30

        )

        self.scheduler.start()

        print("Monitoring Scheduler Started...")