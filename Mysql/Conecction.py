# Mysql/Conecction.py

import mysql.connector

class Connection:
    def __init__(self):
        self.config = {
            "user": "",
            "password": "",
            "host": "",
            "database": "",
        }

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Conexión a MySQL establecida correctamente")
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")

    def close(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("Conexión a MySQL cerrada")
