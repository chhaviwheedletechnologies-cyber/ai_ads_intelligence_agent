from services.google_ads_service import GoogleAdsService


class BudgetOptimizer:

    def __init__(self):

        self.google_ads = GoogleAdsService()

    ##########################################################

    def optimize_budget(self, metrics):

        recommendations = []

        ##################################################

        cost = metrics.get("cost", 0)

        conversions = metrics.get("conversions", 0)

        cpa = metrics.get("cpa", 0)

        roas = metrics.get("roas", 0)

        current_budget = metrics.get("current_budget", 0)

        ##################################################
        # High CPA
        ##################################################

        if cpa > 500:

            recommendations.append({

                "action": "reduce_budget",

                "recommended_budget": current_budget * 0.80,

                "reason": "CPA exceeded threshold."

            })

        ##################################################
        # Good ROAS
        ##################################################

        if roas > 4:

            recommendations.append({

                "action": "increase_budget",

                "recommended_budget": current_budget * 1.20,

                "reason": "Campaign performing well."

            })

        ##################################################
        # No Conversions
        ##################################################

        if conversions == 0 and cost > 3000:

            recommendations.append({

                "action": "pause_budget",

                "recommended_budget": 0,

                "reason": "High spend with zero conversions."

            })

        ##################################################
        # Normal Performance
        ##################################################

        if len(recommendations) == 0:

            recommendations.append({

                "action": "no_change",

                "recommended_budget": current_budget,

                "reason": "Budget is already optimized."

            })

        ##################################################

        return recommendations