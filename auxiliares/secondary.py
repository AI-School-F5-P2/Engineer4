# Se importan las librerías necesarias.
import asyncio
import re # Para identificar símbolos de moneda y separarlos de la cifra en salary
# Se importan los datos de configuración externalizados
from classes.mongo_db import UseMongo
from classes.database import DBAccess
from config.mongo_use import mongo_use

# Creamos la conexión de MongoDB y definimos la base de datos.
# Se le asigna un índice único al campo passport para que no se 
# inserten documentos duplicados.
cliente_mongo = UseMongo() # Creamos un cliente de MongoDB
cliente_mongo.select_db(mongo_use['db'])
cliente_mongo.select_col(mongo_use['collection'])
cliente_mongo.add_index(indexes = ['passport'], uniques = [True])

# Creamos la conexión de MySQL y definimos la estructura de la tabla empleada
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
# Las claves que pueden traer los mensajes se dividen en "relevantes" y "no relevantes".
# La relevantes son aquellas que determinan los datos de una persona de frma única, 
# es decir, determinarán si un mensaje recibido contiene datos asociables a un persona 
# de forma inequívoca.
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

'''
En la función process_message se recibe cada mensaje que llega de main.py, leidos directamente 
de Kafka. Esta función lleva a cabo todo el procesado de mensajes que cubre los siguientes puntos:
    - Recibir el mensaje.
    - Comprobar si, a través de los campos clave, coincide con alguno de los mensajes ya existentes en la lista.
    - Si hay coincidencia, fusiona el mensaje recién recibido con aquél con el que coincide.
    - Si no hay coincidencia, añade el mensaje recién entrrado a lla lista como un mensaje nuevo.

Los mensajes completos tienen, en total, 18 claves. Se consideran completos cuando tienen las 18 con valores.
'''
async def process_message(message):
    '''
    En la lista mensajes_recibidos se almacenan los mensajes que llegan desde la función principal
    y que no coinciden con ninguno de los ya existentes.
    Si el mensaje recibido coincide con alguno que ya hubiera, se fusiona con éste.
    Cuando un mensaje está completo (con las 18 claves) se saca de la lista mensajes_recibidos 
    y se pasa a la lista mensajes_completos.
    '''
    global mensajes_recibidos
    global mensajes_completos

    '''
    La llamada a messsage_depuration pasa el mensaje recién entrado a esa función para cubrir tres aspectos:
        - Si el mensaje tiene la clave sexo, esta viene como una lista de un elemento. 
            Se debe sacar el valor.
        - Si el mensaje tiene la clave salary ha que separar la cifrra del signo 
            de la moneda en salary y currency.
        - Si el mensaje tiene las claves name y last_name, pero no tiene fullname, se construye 
            esta última a partir de las anteriores.
    '''
    message = message_depuration(message)
    # Flag para rastrear si encontramos una coincidencia
    found_match = False
    
    '''
    Se empieza recorriendo cada uno de los mensajes ya existentes en mensajes_recibidos en una 
    enumeración, para tener el mensaje existente como elemento y su índice en la lista.
    '''
    for i, existing_dict in enumerate(mensajes_recibidos):
        '''
        Se recorre la lista de claves relevantes. Serán las que se usen para determinar si el 
        mensaje recibido debe fusionarse con otro mensaje ya existente.
        '''
        for key in claves_relevantes:
            '''
            Se comprueba si cada clave relevante está presente en un mensaje ya existente, 
            y en el mensaje recién recibido, y si en ambos tiene el mismo valor. Eso determinaría 
            que el mensaje recién recibido debe fusionarse con el mensaje existente en proceso.
            '''
            if key in existing_dict and key in message and existing_dict[key] == message[key]:
                # Coincidencia encontrada, fusiona los diccionarios
                existing_dict.update(message)
                found_match = True
                '''
                Si el mensaje previamente existente, después de fusionarle el mensaje recibido, 
                tiene valores en todas las claves, tanto relevantes como no relevantes, 
                se saca de la lista de mensajes_recibidos y se pasa a mensajes_completos.
                '''
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
    
    # Si hay mensajes completados se pasan a la función que los grabará en las bases de datos.
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

    # Después de grabar los mensajes completados en base de datos, se vacía la lista para aligerar la memoria.
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

