import faust
import pandas as pd
import asyncio
from config.kafka_conf import topic, app
from auxiliares.secondary import background_processing

df = pd.DataFrame()


# Iniciar el proceso en segundo plano utilizando create_task
@app.agent(topic)
async def consume_messages(messages):
    asyncio.create_task(background_processing(df))  # Inicia background_processing en segundo plano

    messages_count = 0  # Inicializa el contador a 0
    try:
        async for message in messages:
            messages_count += 1
            print("Mensajes leídos: " + str(messages_count))
            guardar(message)
    except Exception as e:
        print(e)

# faust -A main worker
def guardar(message):
    # Verificar y agregar columnas si no existen
    for columna in message.keys():
        if columna not in df.columns:
            df[columna] = None  # Puedes usar None u otro valor inicial si lo deseas
    # Crear una Serie a partir del diccionario
    serie = pd.Series(message)
    # Agregar la Serie al DataFrame
    df.loc[df.shape[0]] = serie

if __name__ == "__main__":
    app.main()
