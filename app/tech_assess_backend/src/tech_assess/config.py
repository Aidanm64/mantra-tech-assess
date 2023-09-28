import os


def get_mongo_config():
    return {
        "URL": os.getenv("MONGODB_URL"),
        "DB_NAME": os.getenv("MONGODB_DB_NAME")
    }


def get_file_storage_config():

    return {
        "ROOT_FOLDER": "/files"
    }
