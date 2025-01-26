import os
import google.generativeai as genai

GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain",
}


class GeminiClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
            cls._instance.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-thinking-exp-01-21",
                generation_config=GENERATION_CONFIG,
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

        response = self.model.generate_content([prompt, translation])

        try:
            data = response.text
            adjustment, feedback = data.split("---")

            return float(adjustment.strip()), feedback.strip()
        except (ValueError, AttributeError):
            return 0.0, "Unable to evaluate translation at this time."
