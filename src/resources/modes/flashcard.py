from flask_restful import Resource, reqparse
from ...models import Word, mongo
from bson import ObjectId
from ...clients.gemini import GeminiClient

# from ...clients.deepseek import DeepSeekClient


class FlashcardResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "translation", type=str, required=True, help="Translation is required"
        )
        self.gemini = GeminiClient()

        # self.deepseek = DeepSeekClient()

    def get(self):
        try:
            # Use MongoDB's aggregation pipeline to get a random word
            pipeline = [{"$sample": {"size": 1}}]
            random_word = list(mongo.db.words.aggregate(pipeline))

            if not random_word:
                return {"message": "No words found in database"}, 404

            word = random_word[0]
            return {
                "word": {
                    "id": str(word["_id"]),
                    "word": word["word"],
                }
            }, 200

        except Exception as e:
            return {"message": "Error retrieving random word", "error": str(e)}, 500

    def post(self, word_id):
        args = self.parser.parse_args()
        translation = args["translation"]

        try:
            word = Word.get_by_id(word_id)
            if not word:
                return {"message": "Word not found"}, 404

            old_difficulty = word["difficulty"]

            difficulty_adjustment, feedback = self.gemini.evaluate_translation(
                word["word"], translation, old_difficulty
            )

            new_difficulty = max(
                0, min(100, round(old_difficulty + difficulty_adjustment, 2))
            )
            Word.update(word_id, {"difficulty": new_difficulty})

            return {
                "difficulty_change": difficulty_adjustment,
                "new_difficulty": new_difficulty,
                "feedback": feedback,
            }, 200

        except Exception as e:
            return {"message": "Error processing translation", "error": str(e)}, 500
