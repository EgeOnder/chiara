from flask_restful import Resource
from ...models import Word, mongo
from flask import jsonify


class RandomWordResource(Resource):
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
                    "difficulty": word["difficulty"],
                }
            }, 200

        except Exception as e:
            return {"message": "Error retrieving random word", "error": str(e)}, 500
