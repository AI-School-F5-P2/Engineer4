from pymongo import MongoClient

# CONFIGURACION CREENCIALES DE MONGOBD
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "Business"
MONGO_COLLECTION = "negocios16"



# INCIALIZAMAMOS CLIENTE DE MONGO
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# faust -A main worker