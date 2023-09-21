from MongoDB.Conexion import *

# Push data to MongoDB
def push_name(data, name):
    item_to_search = data[name]
    result = db[MONGO_COLLECTION].find_one({"name" : item_to_search})
    if result is None:
        db[MONGO_COLLECTION].insert_one(data)            
    else:
        db[MONGO_COLLECTION].update_one({"name": item_to_search}, {"$set": data})

# Push data to MongoDB
def push_address(data, name):
    item_to_search = data[name]
    result = db[MONGO_COLLECTION].find_one({"Address" : item_to_search})
    if result is None:
        db[MONGO_COLLECTION].insert_one(data)            
    else:
        db[MONGO_COLLECTION].update_one({"Address": item_to_search}, {"$set": data})
    
def push_fullname(data, name):
    item_to_search = data[name]
    result = db[MONGO_COLLECTION].find_one({"Fullname" : item_to_search})
    if result is None:
        db[MONGO_COLLECTION].insert_one(data)            
    else:
        db[MONGO_COLLECTION].update_one({"Fullname": item_to_search}, {"$set": data})


def push_passport(data, name):
    item_to_search = data[name]
    result = db[MONGO_COLLECTION].find_one({"Passport" : item_to_search})
    if result is None:
        db[MONGO_COLLECTION].insert_one(data)            
    else:
        db[MONGO_COLLECTION].update_one({"Passport": item_to_search}, {"$set": data})
        