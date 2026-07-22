import json
from openai import OpenAI

from config.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIService:

    ##########################################################

    def suggest_negative_keywords(self, search_terms):

        if not search_terms:
            return []

        prompt = f"""
        You are a Google Ads optimization expert. Given the following search
        terms report (search term, clicks, conversions), identify which
        search terms are wasting budget and should be added as negative
        keywords. Only flag terms with meaningful clicks and zero conversions.

        Search terms data:
        {json.dumps(search_terms)}

        Respond ONLY with a JSON array, no other text, in this exact format:
        [
          {{"keyword": "...", "reason": "..."}}
        ]

        If none should be flagged, return an empty array [].
        """

        response = client.chat.completions.create(
            model=settings.MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return []

    ##########################################################

    def generate_client_report(self, campaign_data):

        prompt = f"""
        You are an advertising account manager writing a client-facing
        performance report. Based on the data below, write a clear,
        professional summary (3-5 short paragraphs) explaining how the
        campaign performed, what issues were found, what actions were
        taken or recommended, and what to expect next. Avoid technical
        jargon, keep it client-friendly.

        Data:
        {json.dumps(campaign_data, default=str)}
        """

        response = client.chat.completions.create(
            model=settings.MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()