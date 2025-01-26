from flask_restful import Resource, reqparse
from ...models import Word


class WordResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "word", type=str, required=True, help="Word is required"
        )

    def post(self):
        args = self.parser.parse_args()

        print(args)

        # Check if word already exists in the database
        if Word.get_by_word(args["word"]):
            return {"message": "Word already exists"}, 400

        try:
            word_data = {
                "word": args["word"],
                "difficulty": 50,
            }

            result = Word.create(word_data)

            return {
                "message": "Word created successfully",
                "id": str(result.inserted_id),
            }, 201

        except Exception as e:
            return {"message": "Error creating word", "error": str(e)}, 500

    def get(self):
        try:
            words = Word.get_all()
            return {
                "words": [
                    {
                        "id": str(word["_id"]),
                        "word": word["word"],
                        "difficulty": word["difficulty"],
                    }
                    for word in words
                ],
            }, 200
        except Exception as e:
            return {"message": "Error retrieving words", "error": str(e)}, 500
