from flask import Flask
from flask_restful import Api
from .config import Config
from .models import mongo


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize MongoDB
    mongo.init_app(app)

    api = Api(app)

    from .resources import health

    api.add_resource(health.HealthCheck, "/health")

    # Word endpoints
    from .resources.words.words import WordResource
    from .resources.words.random_word import RandomWordResource

    api.add_resource(WordResource, "/words")
    api.add_resource(RandomWordResource, "/words/random")

    # FlashCard mode endpoints
    from .resources.modes.flashcard import FlashcardResource

    api.add_resource(FlashcardResource, "/flashcard", "/flashcard/<word_id>")

    return app
