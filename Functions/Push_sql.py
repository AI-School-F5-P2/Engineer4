import mysql.connector
from Mysql.Conecction import connect, disconnect
import time

connection = connect()
contador = 0

def push_to_sql(data):
    try:
        cursor = connection.cursor()
        # Inserta un nuevo documento en la colección
        sql = "INSERT INTO database_info (id, sex, telfnumber, passport, email, fullname, company, company_address, company_email, company_telfnumber, job, IBAN, salary, address, city, IPv4) VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data.get("sex")[0], data.get("telfnumber"), data.get("passport"), data.get("email"), data.get("fullname"), data.get("company"), data.get("company address"), data.get("company_email"), data.get("company_telfnumber"), data.get("job"), data.get("IBAN"), data.get("salary"), data.get("address"), data.get("city"), data.get("IPv4"))
        cursor.execute(sql, val)
        connection.commit()
        print("Registro insertado correctamente")
    except mysql.connector.Error as e:
        print(f"Error al insertar en la base de datos: {str(e)}")
    finally:
        cursor.close()
        
    
def num_registros():
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM database_info")
    result = cursor.fetchone()[0]
    return result
        





