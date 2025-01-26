import os
from openai import OpenAI


class DeepSeekClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = OpenAI(
                api_key=os.environ.get("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com",
            )
        return cls._instance

    def evaluate_translation(
        self, word: str, translation: str, difficulty_score: float
    ) -> (float, str):
        prompt = f"""
You are a friendly and helpful AI tutor designed to help users learn Italian. The user will be asked to translate words or phrases between English and Italian. Analyse the translation done by the user and adjust the difficulty of the given word below. Adjustment range must be 1-5 points in float. Difficulty score of 100.0 is the **HARDEST** word in the dataset, and the difficulty score of 0.0 is the **EASIEST** word. When a word has a low difficulty score, it means that the user will see less and less of that word because they answered correctly multiple times. So adjust accordingly:
        
- WORD: "{word}"
- DIFFICULTY SCORE: {difficulty_score}

You MUST respond with this structure (if the score is negative, write it with its sign):

<adjustment score float>
---

<Here, give user a very brief feedback considering their response. Be helpful as possible since the user is trying to learn Italian. Do not mention anything about the difficulty score since that is meant only for you and the user will not understand it.>
"""

        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": translation},
            ],
        )

        try:
            data = response.choices[0].message.content

            print(data)

            adjustment, feedback = data.split("---")

            return float(adjustment.strip()), feedback.strip()
        except (ValueError, AttributeError):
            return 0
