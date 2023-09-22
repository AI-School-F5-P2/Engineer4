from MongoDB.Conexion import *

# Push data to MongoDB
def push_name(data, value, clave):
    try:
        result = db[MONGO_COLLECTION].find_one({"passport" : data['passport']})
        result_name_lastname = db[MONGO_COLLECTION].find_one({'fullname': data['name'] + ' ' + data['last_name']})
        if result is None or result_name_lastname is None:
            db[MONGO_COLLECTION].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[MONGO_COLLECTION].update_one({"name": value}, {"$set": new_data})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")

# Push data to MongoDB
def push_address(data, value, clave):
    try:
        result = db[MONGO_COLLECTION].find_one({"address" : value})
        if result is None:
            db[MONGO_COLLECTION].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[MONGO_COLLECTION].update_one({"address": value}, {"$set": new_data})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")
    

# Push data to MongoDB
def push_another(data, value, clave):
    try:
        result = db[MONGO_COLLECTION].find_one({"fullname" : value})
        if result is None:
            db[MONGO_COLLECTION].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[MONGO_COLLECTION].update_one({"fullname": value}, {"$set": new_data})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")

def push_fullname(data, value, clave):
    try:
        result = db[MONGO_COLLECTION].find_one({"fullname" : value})
        if result is None:
            db[MONGO_COLLECTION].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[MONGO_COLLECTION].update_one({"fullname": value}, {"$set": new_data})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")

# Push data to MongoDB
def push_passport(data, value, clave):
    try:
        result = db[MONGO_COLLECTION].find_one({"passport" : value})
        if result is None:
            db[MONGO_COLLECTION].insert_one(data)
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[MONGO_COLLECTION].update_one({"passport": value}, {"$set": new_data})
            # Elimina el segundo documento que no tiene todos los datos
            db[MONGO_COLLECTION].delete_one({"passport": value, clave: {"$exists": False}})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")
