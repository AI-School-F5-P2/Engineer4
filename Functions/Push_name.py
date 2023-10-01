from MongoDB.Conexion import *
from Functions.Push_sql import push_to_sql
# Push data to MongoDB

def push_name(data, value, clave):
    try:
        
        # # Almacena información en las tablas
        # if 'passport' in data:
        #     key = data['passport']
        #     value = data  # Puedes almacenar el diccionario completo
        #     table_passport[key].put(value)
        
        # if 'fullname' in data:
        #     key = data['fullname']
        #     value = data  # Puedes almacenar el diccionario completo
        #     table_fullname[key].put(value)
        
        # # Repite el proceso para otras tablas si es necesario

        # key = data['passport']
        # value = data  # Puedes almacenar el diccionario completo
        # table_passport[key].put(value)

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
            # funcion para comprobar si esta completo el date
            updated_document = db[mongo_collection].find_one({"fullname": value})
            if len(updated_document) == 16:
                print("si entre al if en push name")
                push_to_sql(updated_document)
            else:
                print("no entre al if")
    except Exception as e:
        print(f"push name Error al acceder a la base de datos: {str(e)}")

# Push data to MongoDB
def push_address(data, value, clave):
    try:
        address = data.get("address")
        result = db[mongo_collection].find_one({"address" : address})
        if result is None:
            db[mongo_collection].insert_one(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            db[mongo_collection].update_one({"address": address}, {"$set": new_data})
            # funcion para comprobar si esta completo el date
            updated_document = db[mongo_collection].find_one({"address": address})
            if len(updated_document) == 16:
                print("si entre al if en push_address")
                push_to_sql(updated_document)
            else:
                print("no entre al if")
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
            # funcion para comprobar si esta completo el date
            updated_document = db[mongo_collection].find_one({"fullname": value})
            if len(updated_document) == 16:
                print("si entre al if en push_another")
                push_to_sql(updated_document)
            else:
                print("no entre al if")
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
            # funcion para comprobar si esta completo el date
            updated_document = db[mongo_collection].find_one({"fullname": value})
            if len(updated_document) == 16:
                print("si entre al if en push_fullname")
                push_to_sql(updated_document)
            else:
                print("no entre al if")
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
            # funcion para comprobar si esta completo el date
            updated_document = db[mongo_collection].find_one({"passport": value})
            if len(updated_document) == 16:
                print("si entre al if en push_passport")
                push_to_sql(updated_document)
            else:
                print("no entre al if")
    except Exception as e:
        print(f"push passport Error al acceder a la base de datos: {str(e)}")
        
        
        
        
def push_dataFull(data):
    try:
        db[mongo_collection].insert_one(data)
    except Exception as e:
        print(f"push name Error al acceder a la base de datos: {str(e)}")
