from datetime import datetime

from database.mongo import mongo


class ReportService:

    def __init__(self):

        self.monitoring_collection = mongo.get_collection("monitoring_logs")

        self.execution_collection = mongo.get_collection("execution_logs")

    ##########################################################

    def generate_report(self, campaign_id):

        monitoring_logs = list(

            self.monitoring_collection.find(

                {"campaign_id": campaign_id},

                {"_id": 0}

            )

        )

        execution_logs = list(

            self.execution_collection.find(

                {"campaign_id": campaign_id},

                {"_id": 0}

            )

        )

        ##################################################

        total_spent = 0

        total_clicks = 0

        total_impressions = 0

        total_conversions = 0

        ##################################################

        for log in monitoring_logs:

            total_spent += log.get("cost", 0)

            total_clicks += log.get("clicks", 0)

            total_impressions += log.get("impressions", 0)

            total_conversions += log.get("conversions", 0)

        ##################################################   

        ctr = 0

        if total_impressions > 0:

            ctr = round(

                (total_clicks / total_impressions) * 100,

                2
              
            )

        ##################################################

        cpa = 0

        if total_conversions > 0:

            cpa = round(

                total_spent / total_conversions,

                2

            )

        ##################################################

        report = {

            "campaign_id": campaign_id,

            "generated_at": datetime.utcnow(),

            "summary": {

                "amount_spent": total_spent,

                "clicks": total_clicks,

                "impressions": total_impressions,

                "conversions": total_conversions,

                "ctr": ctr,

                "cpa": cpa

            },

            "monitoring_logs": monitoring_logs,

            "execution_logs": execution_logs

        }

        ##################################################

        return report
    
    ########################################################       
    def get_all_reports(self):

        monitoring_logs = list(

            self.monitoring_collection.find(

                {},

                {"_id": 0}

            )
 
        )

        return {
 
            "total_logs": len(monitoring_logs),

            "logs": monitoring_logs

        }