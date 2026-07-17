from services.google_ads_service import GoogleAdsService


class KeywordOptimizer:

    def __init__(self):

        self.google_ads = GoogleAdsService()

    ##########################################################

    def optimize_keywords(self, campaign_id):

        search_terms = self.google_ads.get_search_terms(campaign_id)

        keywords = self.google_ads.get_keywords(campaign_id)

        recommendations = []

        negative_keywords = []

        ##########################################################
        # Analyze Search Terms
        ##########################################################

        for term in search_terms:

            if (
                term["clicks"] >= 20
                and term["conversions"] == 0
            ):

                negative_keywords.append(
                    term["search_term"]
                )

        ##########################################################
        # Analyze Existing Keywords
        ##########################################################

        for keyword in keywords:

            if (
                keyword["clicks"] >= 30
                and keyword["conversions"] == 0
            ):

                recommendations.append({

                    "keyword": keyword["keyword"],

                    "action": "decrease_bid",

                    "reason": "High clicks but zero conversions."

                })

            elif keyword["conversions"] >= 5:

                recommendations.append({

                    "keyword": keyword["keyword"],

                    "action": "increase_bid",

                    "reason": "High performing keyword."

                })

        ##########################################################
        # Negative Keyword Recommendation
        ##########################################################

        if negative_keywords:

            recommendations.append({

                "action": "add_negative_keywords",

                "keywords": negative_keywords,

                "reason": "Search terms wasting budget."

            })

        ##########################################################
        # No Recommendation
        ##########################################################

        if len(recommendations) == 0:

            recommendations.append({

                "action": "no_change",

                "reason": "Keyword performance is healthy."

            })

        ##########################################################

        return recommendations