import asyncio

# Función asíncrona para procesar y guardar el DataFrame en segundo plano
async def background_processing(df):
    while True:
        print("En el DF: " + str(df.shape[0]))
        await asyncio.sleep(0.2)
