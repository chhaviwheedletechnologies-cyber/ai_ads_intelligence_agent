from pymongo import MongoClient
from config.settings import settings


class MongoDB:

    def __init__(self):

        self.client = MongoClient(settings.MONGO_URI)

        self.db = self.client[settings.DB_NAME]

    def get_collection(self, collection_name):

        return self.db[collection_name]


mongo = MongoDB()