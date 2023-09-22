import json
from Functions.Push_name import push_name, push_address, push_fullname, push_passport, push_another
from Kafka_conexion.Kakfa_con import app, topic
import sys

# funcion para guardar los datos en un json
def save_data(data, path):
    with open(path, "w", encoding="utf-8") as archivo_json:
        json.dump(data, archivo_json, ensure_ascii=False)

# funcion para iterar en la data        
def processData(data):
    try:
    # Procesamos cada data que nos llega y se almacena en bruto
        # save_data(data, "data.json")
        for clave, valor in data.items():
            if 'name' in data and 'last_name' in data and 'sex' in data and 'telfnumber' in data and 'passport' in data and 'email' in data :
                push_name(data, valor, clave)
            elif 'passport' in data and 'IBAN' in data and 'salary' in data :
                push_passport(data, valor, clave)
<<<<<<< HEAD
            elif clave == "fullname":
                push_fullname(data, valor, clave)
            elif "passport" in data:
                push_another(data, valor, clave)
            elif clave == "IPv4":
                push_address(data, valor, clave)
            else:
                pass
=======
            elif 'fullname' in data and 'city' in data and 'address' in data:
                push_fullname(data, valor, clave)
            elif 'fullname' in data and 'company' in data and 'company address' in data and 'company_telfnumber' in data and 'company_email' in data and 'job' in data:
                push_another(data, valor, clave)
            elif 'address' in data and 'IPv4' in data:
                push_address(data, valor, clave)
>>>>>>> bed36bbbec4e05a3b598d800b6c315ebf18a292a
    except Exception as e:
        # print(e)
        pass
        
# Define a Faust table to store consumed data
# faust -A main worker
@app.agent(topic)
async def consume_messages(messages):
<<<<<<< HEAD
    async for message in messages:
        data = message
        processData(data)
        # print(f'Received message: {data}')
        # You can process the message here or store it in a database
=======
    '''Consume messages from a Kafka topic
    To start the application enter the following command: 
    faust -A main worker
    '''
    try:
        async for message in messages:
            data = message
            processData(data)
            print(f'Received message: {data}')
    except Exception as e:
        print(e)
>>>>>>> bed36bbbec4e05a3b598d800b6c315ebf18a292a
