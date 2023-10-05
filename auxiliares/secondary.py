import asyncio
from classes.mongo_db import UseMongo
from classes.database import DBAccess
import re # Para identificar símbolos de moneda y separarlos de la cifra en salary
from config.mongo_use import mongo_use

# Creamos la conexión de MongoDB
cliente_mongo = UseMongo() # Creamos un cliente de MongoDB
cliente_mongo.select_db(mongo_use['db'])
cliente_mongo.select_col(mongo_use['collection'])
cliente_mongo.add_index(indexes = ['passport'], uniques = [True])

# Creamos la conexión de MySQL
sql = DBAccess()
sql.create_connection()
sql.create_cursor()
sql.select_database("data_engineer")
tabla_de_sql = "datos_mongo"
campos_de_sql = [
    "name",
    "last_name",
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

##### INFORMACIÓN SOBRE LA ESTRUCTURA DE LOS MENSAJES DE KAFKA
claves_relevantes = ['passport', 'IBAN', 'fullname', 'company_email', 'telfnumber', 'email', 'IPv4', 'address']
claves_no_relevantes = ['salary', 'currency', 'city', 'company', 'company address', 'company_telfnumber', 'job', 'name', 'last_name', 'sex']
tipos_de_mensajes = [
    ['name', 'last_name', 'sex', 'telfnumber', 'passport', 'email', 'fullname'],
    ['fullname', 'company', 'company address', 'company_telfnumber', 'company_email', 'job'],
    ['address', 'IPv4'],
    ['passport', 'IBAN', 'salary']
]

mensajes_recibidos = [] # Donde se van almacenando y fusionando los mensajes que van llegando
mensajes_completos = [] # Donde se van trasladando los mensajes que se han completado
# Función asíncrona para procesar y guardar el DataFrame en segundo plano

async def process_message(message):
    global mensajes_recibidos
    global mensajes_completos

    message = message_depuration(message)
    # Flag para rastrear si encontramos una coincidencia
    found_match = False
    
    for i, existing_dict in enumerate(mensajes_recibidos):
        for key in claves_relevantes:
            if key in existing_dict and key in message and existing_dict[key] == message[key]:
                # Coincidencia encontrada, fusiona los diccionarios
                existing_dict.update(message)
                found_match = True
                if len(existing_dict) == len(claves_relevantes) + len(claves_no_relevantes):
                    mensajes_completos.append(existing_dict)
                    mensajes_recibidos.pop(i)
                break
        if found_match:
            break

    # Si no se encontró ninguna coincidencia, agrega el nuevo diccionario
    if not found_match:
        if len (message) == len(claves_relevantes) + len(claves_no_relevantes):
            mensajes_completos.append(message)
        else:
            mensajes_recibidos.append(message)
    
    if len (mensajes_completos) > 0:
        await save_in_databases()

    return

async def save_in_databases():
    global mensajes_completos
    for completado in mensajes_completos:
        cliente_mongo.insert(completado)
        query = f"INSERT INTO {tabla_de_sql} ({', '.join(campos_de_sql)}) VALUES ({', '.join(['%s'] * len(campos_de_sql))})"
        argumentos = [
            completado['name'],
            completado['last_name'],
            completado['fullname'],
            completado['city'], 
            completado['address'], 
            completado['telfnumber'], 
            completado['email'], 
            completado['sex'], 
            completado['passport'], 
            completado['IBAN'], 
            completado['salary'], 
            completado['currency'], 
            completado['IPv4'], 
            completado['company'], 
            completado['company address'], 
            completado['company_telfnumber'], 
            completado['company_email'], 
            completado['job']
        ]
        sql.set_data(query, argumentos)

    mensajes_completos = []
    return

def message_depuration(message):
    # Si existen los campos name y last_name, y no existe full_name, 
    # lo creamos a partir de name y last_name.
    if "name" in message and "last_name" in message and "fullname" not in message:
        message["fullname"] = message["name"] + " " + message["last_name"]
    # Si existe el sexo, viene como una lista. lo extraemos para que sea un elemento como los demás.
    # El sexo puede venir como de tipo None, así que hay que tener eso en cuenta.
    if "sex" in message:
        if type(message["sex"]) != type(None):
            message["sex"] = message["sex"][0]
        else:
            message["sex"] = "ND"
    # Si existe el campo salary tenemos que separar la cifra del símbolo de moneda.
    # Eso lo hacemos para facitilar luego a los data analist el procesado de datos.
    if "salary" in message:
        match = re.match(r'(\d+)(\D+)', message["salary"])
        message["salary"] = match.group(1)
        message["currency"] = match.group(2)
    return message

