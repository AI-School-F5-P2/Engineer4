import mysql.connector
from decouple import config

host = config("HOST")
user = config("USER_SQL")
password = config("PASSWORD")
database = config("DATABASE_SQL")
connection = None

def connect():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Conexión a MySQL establecida correctamente")
            return connection
        else:
            print("No se pudo establecer la conexión a MySQL")
    except mysql.connector.Error as e:
        print(f"Error al acceder a la base de datos: {str(e)}")

def disconnect():
    if connection and connection.is_connected():
        connection.close()
        print("Conexión a MySQL cerrada")