'''
Para poner en marcha:
    Activar Docker Desktop.
    En la terminal escribir: docker-compose up --build
    Cuando veamos en Docker Desktop el container en verde, teclear, en otra terminal:
    faust -A main worker
'''

import asyncio
# Se importa desde el paquete config un fichero con los datos de conexión y 
# las variables de uso, para tener esta información externalizada. 
from config.kafka_conf import topic, app
from auxiliares.secondary import process_message

# Este es el proceso principal que se ocupa de leer los mensajes de Kafka
# Y pasarlos a una función donde se procesan.
@app.agent(topic)
async def consume_messages(messages):
    try:
        async for message in messages:
            # Iniciar el proceso en segundo plano utilizando process_message
            await process_message(message)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.main()


# faust -A main worker

