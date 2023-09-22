from pymongo import MongoClient
from decouple import config

mongo_url = config("MONGO_URL")
mongo_database = config("MONGO_DATABASE")
mongo_collection = config("MONGO_COLLECTION")

# INCIALIZAMAMOS CLIENTE DE MONGO
client = MongoClient(mongo_url)
db = client[mongo_database]

# faust -A main worker
