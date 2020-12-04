from pymongo import MongoClient


class QueueDB:
    _instance = None

    def __init__(self):
        self.client = MongoClient(port=27017)
        self.queue_db = self.client.trena

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def database():
        return QueueDB.instance().queue_db
