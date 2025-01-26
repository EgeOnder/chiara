from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()


class Word:
    def __init__(self, word, difficulty):
        self.word = word
        self.difficulty = difficulty

    @staticmethod
    def create(word_data):
        return mongo.db.words.insert_one(word_data)

    @staticmethod
    def get_all():
        return list(mongo.db.words.find())

    @staticmethod
    def get_by_id(word_id):
        return mongo.db.words.find_one({"_id": ObjectId(word_id)})

    @staticmethod
    def get_by_word(word):
        return mongo.db.words.find_one({"word": word})

    @staticmethod
    def update(word_id, word_data):
        return mongo.db.words.update_one(
            {"_id": ObjectId(word_id)}, {"$set": word_data}
        )

    @staticmethod
    def delete(word_id):
        return mongo.db.words.delete_one({"_id": ObjectId(word_id)})
