from MongoDB.Conexion import *

# Push data to MongoDB
def push_name(data, value, clave):
    try:
        name = data.get("name", "")
        last_name = data.get("last_name", "")
        data['fullname'] = f"{name} {last_name}"
        # Elimino las columnas
        del data['name']
        del data['last_name']
        
        result = db[mongo_collection].find_one({"fullname" : value})
        if result is None:
            db[mongo_collection].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[mongo_collection].update_one({"fullname": value}, {"$set": new_data})
    except Exception as e:
        print(f"push name Error al acceder a la base de datos: {str(e)}")

# Push data to MongoDB
def push_address(data, value, clave):
    try:
        address = data.get("address")
        result = db[mongo_collection].find_one({"address" : address})
        print(result)
        if result is None:
            db[mongo_collection].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[mongo_collection].update_one({"address": address}, {"$set": new_data})
    except Exception as e:
        print(f"push adres Error al acceder a la base de datos: {str(e)}")
    

# Push data to MongoDB
def push_another(data, value, clave):
    try:
        result = db[mongo_collection].find_one({"fullname" : value})
        if result is None:
            db[mongo_collection].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[mongo_collection].update_one({"fullname": value}, {"$set": new_data})
    except Exception as e:
        print(f"push anoter Error al acceder a la base de datos: {str(e)}")
        
        
        

def push_fullname(data, value, clave):
    try:
        result = db[mongo_collection].find_one({"fullname" : value})
        if result is None:
            db[mongo_collection].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[mongo_collection].update_one({"fullname": value}, {"$set": new_data})
    except Exception as e:
        print(f"push name Error al acceder a la base de datos: {str(e)}")

# Push data to MongoDB
def push_passport(data, value, clave):
    try:
        result = db[mongo_collection].find_one({"passport" : value})
        if result is None:
            db[mongo_collection].insert_one(data)
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[mongo_collection].update_one({"passport": value}, {"$set": new_data})
            # Elimina el segundo documento que no tiene todos los datos
            db[mongo_collection].delete_one({"passport": value, clave: {"$exists": False}})
    except Exception as e:
        print(f"push passport Error al acceder a la base de datos: {str(e)}")
