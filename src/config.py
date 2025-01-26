import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://localhost:27017/chiara"
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
    TESTING = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True
