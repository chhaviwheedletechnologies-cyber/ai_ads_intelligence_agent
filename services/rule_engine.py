from config.settings import settings


class RuleEngine:

    def __init__(self):

        self.cpa_threshold = settings.CPA_THRESHOLD
        self.ctr_threshold = settings.CTR_THRESHOLD
        self.roas_threshold = settings.ROAS_THRESHOLD

        self.conversion_rate_threshold = 2.0
        self.average_cpc_threshold = 30
        self.average_cpm_threshold = 250
        self.amount_spent_threshold = 5000

    ########################################################

    def evaluate(self, metrics):

        actions = []

        ########################################################
        # CPA
        ########################################################

        if metrics.get("cpa", 0) > self.cpa_threshold:

            actions.append({

                "action": "pause_campaign",

                "reason": f"High CPA ({metrics['cpa']})"

            })

        ########################################################
        # CTR
        ########################################################

        if metrics.get("ctr", 0) < self.ctr_threshold:

            actions.append({

                "action": "optimize_keywords",

                "reason": f"Low CTR ({metrics['ctr']})"

            })

        ########################################################
        # ROAS
        ########################################################

        if metrics.get("roas", 0) < self.roas_threshold:

            actions.append({

                "action": "reduce_budget",

                "reason": f"Low ROAS ({metrics['roas']})"

            })

        ########################################################
        # Conversion Rate
        ########################################################

        if metrics.get("conversion_rate", 0) < self.conversion_rate_threshold:

            actions.append({

                "action": "improve_targeting",

                "reason": f"Low Conversion Rate ({metrics['conversion_rate']})"

            })

        ########################################################
        # Average CPC
        ########################################################

        if metrics.get("average_cpc", 0) > self.average_cpc_threshold:

            actions.append({

                "action": "decrease_keyword_bid",

                "reason": f"High Average CPC ({metrics['average_cpc']})"

            })

        ########################################################
        # Average CPM
        ########################################################

        if metrics.get("average_cpm", 0) > self.average_cpm_threshold:

            actions.append({

                "action": "optimize_audience",

                "reason": f"High Average CPM ({metrics['average_cpm']})"

            })

        ########################################################
        # Amount Spent
        ########################################################

        if metrics.get("amount_spent", 0) > self.amount_spent_threshold:

            actions.append({

                "action": "review_budget",

                "reason": f"High Spend ({metrics['amount_spent']})"

            })

        ########################################################
        # No Conversions
        ########################################################

        if metrics.get("conversions", 0) == 0:

            actions.append({

                "action": "pause_campaign",

                "reason": "No conversions detected."

            })

        ########################################################

        if not actions:

            actions.append({

                "action": "no_action",

                "reason": "Campaign performing normally."

            })

        return actions
    