import asyncio
import pandas as pd
from classes.mongo_db import UseMongo
from classes.database import DBAccess
import re # Para identificar símbolos de moneda y separarlos de la cifra en salary

# Creamos la conexión de MongoDB
cliente_mongo = UseMongo() # Creamos un cliente de MongoDB
cliente_mongo.select_db('mensajes')
cliente_mongo.select_col('mensajes_recibidos')
cliente_mongo.add_index(indexes = ['passport'], uniques = [True])

# Creamos la conexión de MySQL
sql = DBAccess()
sql.create_connection()
sql.create_cursor()
sql.select_database("data_engineer")
tabla_de_sql = "datos_mongo"
campos_de_sql = [
    "fullname",
    "city",
    "address",
    "telf_number",
    "email",
    "sex", 
    "passport",
    "iban",
    "salary",
    "currency",
    "ipv4",
    "company",
    "company_address",
    "company_telfnumber",
    "company_email",
    "job"
]

# Define un contador para mensajes procesados en secondary.py
message_counter = 0
posibles_claves = {
    "passport": True,
    "IBAN": True,
    "salary": False, 
    "fullname": True, 
    "city": False,
    "address": False, 
    "IPv4": False,
    "company": False,
    "company address": False,
    "company_telfnumber": False,
    "company_email": True,
    "job": False,
    "name": False,
    "last_name": False,
    "sex": False,
    "telfnumber": True,
    "email": True
}
claves_relevantes = ['passport', 'IBAN', 'fullname', 'company_email', 'telfnumber', 'email', 'IPv4', 'address']
claves_no_relevantes = ['salary', 'city', 'company', 'company address', 'company_telfnumber', 'job', 'name', 'last_name', 'sex']
tipos_de_mensajes = [
    ['name', 'last_name', 'sex', 'telfnumber', 'passport', 'email', 'fullname'],
    ['fullname', 'company', 'company address', 'company_telfnumber', 'company_email', 'job'],
    ['address', 'IPv4'],
    ['passport', 'IBAN', 'salary']
]

'''
Vale. Ya tenemos el diccionario de claves con las posibles condiciones de relevante o no relevante, así:
Ahora tenemos que tener en cuenta lo siguiente:
- No todos los mensajes contienen todos los datos. Algunos mensajes contienen unos datos, y otros mensajes contienen otros datos.
- Hay datos "especiales" como name y last_name. Por sí solos no son relevantes, pero si están esos dos datos en un mensaje, y no contiene fullname, se construirá fullname a partir de name + " " + last_name, y fullname sí es relevante.

El procesado es el siguiente: una vez revisada esa posible construcción de fullname, 
si es el caso, se comprobará cada dato relevante. 
Por ejemplo, IBAN se buscará en la columna IBAN del DF. Si el DF aún no tiene esa  '''


# Función asíncrona para procesar y guardar el DataFrame en segundo plano

async def process_message(df, message):
    mensaje_grabado = False # El mensaje aún no se ha grabado en el df
    '''
    En primer lugar filtramos los datos que lo necesitan:
        Si no existe el fullname, pero sí el name y el last_name, los concatenamos para 
        formar el fullname, ya que ese sí es un campo clave para la unicidad de registros.
        Si existe el sexo, que viene como una lista de un elemento,
        lo conversitmos a una cadena "normal", para poder grabarlo.
        Por último, si en el mensaje viene el campo salary, separamos la cifra de la 
        abreviación de moneda, y lo metemos en dos campos aparte.
    '''
    # Si existen los campos name y last_name, y no existe full_name, 
    # lo creamos a partir de name y last_name.
    if "name" in message and "last_name" in message and "fullname" not in message:
        message["fullname"] = message["name"] + " " + message["last_name"]
    # Si existe el sexo, viene como una lista. lo extraemos para que sea un elemento como los demás.
    # El sexo puede venir como de tipo None, así que hay que tener eso en cuenta.
    if "sex" in message:
        if type(message["sex"]) != type(None):
            message["sex"] = message["sex"][0]
    # Si existe el campo salary tenemos que separar la cifra del símbolo de moneda.
    # Eso lo hacemos para facitilar luego a los data analist el procesado de datos.
    if "salary" in message:
        match = re.match(r'(\d+)(\D+)', message["salary"])
        message["salary"] = match.group(1)
        message["currency"] = match.group(2)
    '''
    Ahora procesamos el mensaje para determinar si deben unirse sus datos a los de algún mensaje ya 
    existente en el DF. La clave para determinar esto es identificar si alguno de los campos relevantes 
    de la unicidad del mensaje existe ya en el DF con el mismo valor.
    En ese caso, ambos mensajes (el ya existente en el DF y el que estamos procesando) se fusionarán en 
    una sola fila en el DF.
    '''
    # Determinamos si el mensaje tiene claves relevantes.
    # Si no es así, terminamos esta función.
    claves_del_mensaje = message.keys()
    if not any(elemento in claves_del_mensaje for elemento in claves_relevantes):
        return
    # Ahora reviso cada clave relevante del mensaje, para ver si 
    # el valor asociado está en la correspondiente columna del DF.
    for clave in claves_del_mensaje:
        if not clave in claves_relevantes:
            continue # Si la clave no está en claves_relevantes, no me interesa seguir trabajando con ese valor.
        valor = str(message[clave])
        if df[clave].isin([valor]).any():
            indice_fila = df[clave].isin([valor]).idxmax()
            df.loc[indice_fila, claves_del_mensaje] = message
            mensaje_grabado = True # El mensaje se ha grabado en el DF
            break
    # Si el mensaje no se ha grabado aún en el DF, se graba ahora en una fila nueva
    if not mensaje_grabado:
        serie = pd.Series(message)
        df.loc[df.shape[0]] = serie

    await send_to_mongo(df)


async def send_to_mongo(df):
    filas_eliminadas = None
    '''
        En este proceso se determina que hacer con las filas del DF para pasarlas 
        a MongoDB y a SQL.
        Al pasar una fila del DF a las bases de datos esa fila se elimina de dicho DF,
        por lo que es necesario establecer un criterio.
        No se puede establecer como criterio el que las filas estén absolutamente completadas,
        porque ese caso no se va a dar.
        Probablemente se pueda establecer como criterio que las filas tengan 
        todos los campos relevantes completados.
    '''

    # # Paso 1: Verifica si todas las columnas (claves) tienen contenido en cada fila
    filas_con_todos_los_campos_cumplimentados = df.notna().all(axis=1)
    filas_eliminadas = df[filas_con_todos_los_campos_cumplimentados]

    # Eliminar las filas del DF original
    df = df[~filas_con_todos_los_campos_cumplimentados]

    # Paso 2: Insertar las filas eliminadas en la base de datos de Mongo
    if not filas_eliminadas.empty:
        records = filas_eliminadas.to_dict(orient='records')
        cliente_mongo.insert(records)  # Insertar las filas en la colección de Mongo# Filtra el DataFrame original para obtener las filas que cumplen con el criterio
        await send_to_sql(records)
    del filas_eliminadas

async def send_to_sql(records):
    for record in records:
        query = f"INSERT INTO {tabla_de_sql} ({', '.join(campos_de_sql)}) VALUES ({', '.join(['%s'] * len(campos_de_sql))})"
        argumentos = [
            record['fullname'],
            record['city'], 
            record['address'], 
            record['telfnumber'], 
            record['email'], 
            record['sex'], 
            record['passport'], 
            record['IBAN'], 
            record['salary'], 
            record['currency'], 
            record['IPv4'], 
            record['company'], 
            record['company address'], 
            record['company_telfnumber'], 
            record['company_email'], 
            record['job']
        ]

        sql.set_data(query, argumentos)

