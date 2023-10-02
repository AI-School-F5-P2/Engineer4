'''
Para poner en marcha:
    Activar Docker Desktop.
    En la terminal escribir: docker-compose up --build
    Cuando veamos en Docker Desktop el container en verde, teclear, en otra terminal:
    faust -A main worker
'''

import faust
import concurrent.futures
import pandas as pd
import asyncio
from config.kafka_conf import topic, app
from auxiliares.secondary import process_message

columnas = [
    "passport",
    "IBAN",
    "salary",
    "currency",
    "fullname",
    "city",
    "address",
    "IPv4",
    "company",
    "company address",
    "company_telfnumber",
    "company_email",
    "job",
    "name",
    "last_name",
    "sex",
    "telfnumber",
    "email"
]

df = pd.DataFrame(columns = columnas)

# Iniciar el proceso en segundo plano utilizando create_task
@app.agent(topic)
async def consume_messages(messages):
    try:
        async for message in messages:
            await process_message(df, message)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.main()


# faust -A main worker

