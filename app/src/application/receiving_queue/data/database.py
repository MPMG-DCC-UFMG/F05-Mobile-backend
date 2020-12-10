from pymongo import MongoClient

from application.core import config

class QueueDB:
    _instance = None

    def __init__(self):
        if config.settings.environment == "development":
            mongoClient = MongoClient(port=27017)
        else:
            mongoClient = MongoClient('mongodb', 27017)
        self.client = mongoClient
        self.queue_db = self.client.trena

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def database():
        return QueueDB.instance().queue_db
