from Mysql.Conecction import Connection
import time

def push_to_sql(data):
    try:
        # Establece la conexión a la base de datos
        connection = Connection()
        if connection.is_connected():
            print("Conexión a MySQL establecida correctamente")
            time.sleep(5)
            # Aquí puedes realizar operaciones con la base de datos
            cursor = connection.cursor()
            # Inserta un nuevo documento en la colección
            sql = "INSERT INTO datos_mongo (`sex`, `telfnumber`, `passport`, `email`, `fullname`, `company`, `company_address`, `company_email`, `company_telfnumber`, `job`, `IBAN`, `salary`, `address`, `city`, `IPv4`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (data.get("sex"), data.get("telfnumber"), data.get("passport"), data.get("email"), data.get("fullname"), data.get("company"), data.get("company address"), data.get("company_email"), data.get("company_telfnumber"), data.get("job"), data.get("IBAN"), data.get("salary"), data.get("address"), data.get("city"), data.get("IPv4"))
            cursor.execute(sql, val)

            connection.commit()
            print("1 record inserted, ID:", cursor.lastrowid)
            # connection.close()
    except Exception as e:
        print(f"push to sql Error al acceder a la base de datos: {str(e)}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión a MySQL cerrada")
