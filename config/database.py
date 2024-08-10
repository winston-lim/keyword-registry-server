from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from . import config

settings = config.get_settings()
db = None

def get_database():
    global db
    if db is not None:
        return db
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(settings.mongo_url, username=settings.mongo_username, password=settings.mongo_password)
    try:
        # The ismaster command is cheap and does not require auth.
        print(client.server_info())
    except ConnectionFailure:
        print("Server not available")
    db = client[settings.mongo_database]
    return db