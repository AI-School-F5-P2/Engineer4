from kafka import KafkaConsumer
import json


# Configura los parámetros de conexión a Kafka
bootstrap_servers = 'localhost:29092'  # Reemplaza con la dirección de tu servidor Kafka
topic_name = 'probando'  # Reemplaza con el nombre del tópico de Kafka

# Crea un consumidor de Kafka
consumer = KafkaConsumer(topic_name, group_id='my-group', bootstrap_servers=bootstrap_servers)

# Define una función para guardar los datos en un archivo JSON
def guardar_data(data):
    # Decodifica los datos de bytes a una cadena (string)
    data_str = data.decode('utf-8')

    # Convierte la cadena 'data_str' a un diccionario
    data_dict = json.loads(data_str)

    with open('datos.json', 'a') as archivo_json:
        # Convierte el diccionario 'data_dict' a formato JSON y guárdalo en el archivo
        json.dump(data_dict, archivo_json)
        archivo_json.write('\n')  # Agrega una nueva línea después de cada registro JSON
        
    

# Itera sobre los mensajes y procesa los datos
for message in consumer:
    data = message.value  # Los datos del mensaje
    # Realiza acciones de procesamiento aquí
    guardar_data(data)
    print(data)
    



     # Los datos del mensaje
    # Realiza acciones de procesamiento aquí
    # guardar_data(data)
    # print(data.fullname)
    
     