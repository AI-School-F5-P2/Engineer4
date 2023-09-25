#import json
#from auxiliares.Push_name import push_name, push_address, push_fullname, push_passport, push_another
from conf.kafka_conf import app, topic

# funcion para guardar los datos en un json
#def save_data(data, path):
#    with open(path, "w", encoding="utf-8") as archivo_json:
#        json.dump(data, archivo_json, ensure_ascii=False)

        # faust -A main worker
# Define a Faust table to store consumed data

@app.agent(topic)
async def consume_messages(messages):
    try:
        async for message in messages:
            data = message
            #processData(data)
            print(f'Received message: {data}')
    except Exception as e:
        print(e)
