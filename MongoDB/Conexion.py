from pymongo import MongoClient

# CONFIGURACION CREENCIALES DE MONGOBD
MONGO_URI = ""
MONGO_DB = ""
MONGO_COLLECTION = ""




# INCIALIZAMAMOS CLIENTE DE MONGO
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]