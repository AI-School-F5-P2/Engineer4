import faust
import json
from Functions.Push_name import push_name, push_address, push_fullname, push_passport, push_another
from Kafka_conexion.Kakfa_con import app, topic

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
            if clave == 'name':
                push_name(data, valor, clave)
            elif clave == 'passport':
                push_passport(data, valor, clave)
            elif clave == "Fullname":
                push_fullname(data, valor, clave)
            elif "Passport" in data:
                push_another(data, valor, clave)
            elif clave == "Address":
                push_address(data, clave)
            else:
                pass
    except Exception as e:
        print(e)
        pass
        
# Define a Faust table to store consumed data
@app.agent(topic)
async def consume_messages(messages):
    async for message in messages:
        data = message
        processData(data)
        print(f'Received message: {data}')
        # You can process the message here or store it in a database