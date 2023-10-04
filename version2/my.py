import faust
from decouple import config

# Configuración sencilla de Faust utilizando la configuración importada
app = faust.App(
    config("BROKER_URL"),
    broker=config("COMSUMER"), 
    value_serializer=config("FORMAT"),
)

topic = app.topic(config("TOPIC"))

total_data = {}

def generate_compound_key(data):
    # Genera una clave compuesta utilizando el nombre, pasaporte y dirección
    nombre = data.get("fullname")
    pasaporte = data.get("passport")
    address = data.get("address")
    return f"{nombre}_{pasaporte}_{address}"

def processData(data):
    compound_key = generate_compound_key(data)

    if compound_key in total_data:
        # Si la clave compuesta ya existe, verifica si todos los registros están unificados
        registro_existente = total_data[compound_key]
        if all(value == registro_existente.get(key) for key, value in data.items()):
            # Si todos los registros coinciden, no se hace nada
            pass
        else:
            # Si no todos los registros coinciden, se emite una advertencia
            print(f"Advertencia: Registros no unificados para '{compound_key}':")
            print("Registros existentes:")
            print(registro_existente)
            print("Nuevo registro:")
            print(data)
            print()
    else:
        # Si la clave compuesta no existe, agrega un nuevo registro
        total_data[compound_key] = data

    # Imprime los registros unificados
    print("*****")
    print(f"Registros unificados para '{compound_key}':")
    print("*****")
    for clave, registro in total_data.items():
        print("______")
        print(clave)
        print(registro)
        print("_______")
    print()

@app.agent(topic)
async def consume_messages(messages):
    '''Consume messages from a Kafka topic
    To start the application enter the following command: 
    faust -A main worker
    '''
    try:
        async for message in messages:
            data = message
            processData(data)
            # print(f'Received message: {data}')
    except Exception as e:
        # print(e)
        pass

# Iniciar la aplicación Faust
if __name__ == "__main__":
    app.main()
