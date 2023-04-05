import pymongo
from logger import logger
from dotenv import load_dotenv
import os
load_dotenv()

def get_db():
    pmongo = pymongo.MongoClient(os.getenv["MONGO_URI"], serverSelectionTimeoutMS=5000)
    _db = pmongo[os.getenv["MONGO_DATABASE"]]
    logger.info(f"Connecting to DB: {os.getenv['MONGO_URI']}")
    logger.info(f"Connection state: {pmongo.server_info()}")
    return _db


db = get_db()
print(db,'=======')