import pymongo
from tech_assess.config import get_mongo_config


def get_database():
    cfg = get_mongo_config()
    client = pymongo.MongoClient(cfg['URL'])
    return client[cfg['DB_NAME']]

