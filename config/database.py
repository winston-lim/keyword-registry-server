from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from . import config

settings = config.get_settings()
client = None

def get_client():
    global client
    if client is not None:
        return client
    client = MongoClient(settings.mongo_url, username=settings.mongo_username, password=settings.mongo_password)
    try:
        print(client.server_info())
    except ConnectionFailure:
        print("Mongo server not available")
    return client