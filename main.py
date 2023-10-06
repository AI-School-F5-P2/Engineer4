'''
Para poner en marcha:
    Activar Docker Desktop.
    En la terminal escribir: docker-compose up --build
    Cuando veamos en Docker Desktop el container en verde, teclear, en otra terminal:
    faust -A main worker
'''

import asyncio
from config.kafka_conf import topic, app
from auxiliares.secondary import process_message

# Iniciar el proceso en segundo plano utilizando create_task
@app.agent(topic)
async def consume_messages(messages):
    try:
        async for message in messages:
            await process_message(message)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.main()


# faust -A main worker

