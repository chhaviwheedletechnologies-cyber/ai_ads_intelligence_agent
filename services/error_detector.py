class ErrorDetector:

    def detect_performance_errors(self, metrics):

        errors = []

        if metrics is None:
            return errors

        cost = metrics.get("cost", 0)
        conversions = metrics.get("conversions", 0)
        clicks = metrics.get("clicks", 0)
        impressions = metrics.get("impressions", 0)
        cpa = metrics.get("cpa", 0)

        if cost > 3000 and conversions == 0:
            errors.append({
                "type": "performance",
                "issue": "high_spend_zero_conversions",
                "detail": f"Spent {cost} with zero conversions."
            })

        if cpa > 500:
            errors.append({
                "type": "performance",
                "issue": "high_cpa",
                "detail": f"CPA is {cpa}, exceeds threshold of 500."
            })

        if impressions > 1000 and clicks == 0:
            errors.append({
                "type": "performance",
                "issue": "zero_clicks_high_impressions",
                "detail": f"{impressions} impressions but zero clicks. Possible targeting or creative issue."
            })

        return errors

    ##########################################################

    def detect_policy_errors(self, policy_issues):

        errors = []

        for issue in policy_issues:
            errors.append({
                "type": "policy",
                "issue": issue.get("type", "policy_issue"),
                "detail": issue.get("detail", "Policy issue detected.")
            })

        return errors