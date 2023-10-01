from mongo_conexion import *


def push_dataFull(data):
    try:
        db[mongo_collection].insert_one(data)
    except Exception as e:
        print(f"push name Error al acceder a la base de datos: {str(e)}")