import json

from openai import OpenAI

from config.settings import settings

from prompts.analysis_prompt import ANALYSIS_PROMPT


class AIAnalysisService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    ##################################################

    def analyze(self, metrics):

        prompt = ANALYSIS_PROMPT.format(
            metrics=json.dumps(metrics, indent=2)
        )

        response = self.client.chat.completions.create(

            model=settings.MODEL,

            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],

            temperature=0.2

        )

        content = response.choices[0].message.content

        try:

            return json.loads(content)

        except Exception:

            return {

                "status": "failed",

                "raw_response": content

            }