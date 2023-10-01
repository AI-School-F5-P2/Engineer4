import mysql.connector
from Mysql.Conecction import connect, disconnect

connection = connect()
contador = 0

def push_to_sql(data):
    try:
        cursor = connection.cursor()
        # Inserta un nuevo documento en la colección
        sql = "INSERT INTO data_full (id, sex, telfnumber, passport, email, fullname, city, address, company, company_address,  company_telfnumber, company_email, job, IBAN, salary, IPv4) VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data.get("sex")[0], data.get("telfnumber"), data.get("passport"), data.get("email"), data.get("fullname"), data.get("city"), data.get("address"), data.get("company"), data.get("company address"), data.get("company_telfnumber"), data.get("company_email"), data.get("job"), data.get("IBAN"), data.get("salary"), data.get("IPv4"))
        cursor.execute(sql, val)
        connection.commit()
        print("Registro insertado correctamente")
    except mysql.connector.Error as e:
        print(f"Error al insertar en la base de datos: {str(e)}")
    finally:
        cursor.close()