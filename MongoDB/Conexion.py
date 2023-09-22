from pymongo import MongoClient
from decouple import config

# CONFIGURACION CREENCIALES DE MONGOBD
MONGO_URI = config("MONGO_URI")
MONGO_DB = config("MONGO_DB")
MONGO_COLLECTION = config("MONGO_COLLECTION")


# INCIALIZAMAMOS CLIENTE DE MONGO
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]