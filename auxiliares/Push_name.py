from classes.mongo_db import UseMongo
from conf.mongo_conn import *
from conf.mongo_use import *

mi_cliente = UseMongo(
    server=mongo_data['server'], 
    port=mongo_data['port'], 
    user=mongo_data['user'], 
    password=mongo_data['password']
)

# Push data to MongoDB
def push_name(data, value, clave):
    try:
        result = mi_cliente.select_docs({"passport" : data['passport']})
        result_name_lastname = mi_cliente.select_docs({'fullname': data['name'] + ' ' + data['last_name']})
        if result is None or result_name_lastname is None:
            mi_cliente.insert(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            mi_cliente.change_docs({"name": value}, {new_data})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")

# Push data to MongoDB
def push_address(data, value, clave):
    try:
        result = mi_cliente.select_docs({"address" : value})
        if result is None:
            mi_cliente.insert(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            mi_cliente.change_docs({"address": value}, {new_data})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")
    

# Push data to MongoDB
def push_another(data, value, clave):
    try:
        result = mi_cliente.select_docs({"fullname" : value})
        if result is None:
            mi_cliente.insert(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            mi_cliente.change_docs({"fullname": value}, {new_data})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")

def push_fullname(data, value, clave):
    try:
        result = mi_cliente.select_docs({"fullname" : value})
        if result is None:
            mi_cliente.insert(data)            
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            mi_cliente.change_docs({"fullname": value}, {new_data})
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")

# Push data to MongoDB
def push_passport(data, value, clave):
    try:
        result = mi_cliente.select_docs({"passport" : value})
        if result is None:
            mi_cliente.insert(data)
        else:
            new_data = {**result, **data}
            # Actualiza el documento en la base de datos con los nuevos datos
            mi_cliente.change_docs({"passport": value}, {new_data}, one = True)
            # Elimina el segundo documento que no tiene todos los datos
            mi_cliente.remove_docs({"passport": value}, one = True)
    except Exception as e:
        print(f"Error al acceder a la base de datos: {str(e)}")
