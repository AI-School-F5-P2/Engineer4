BROKER_URL = '' # El broker de Kafka
COMSUMER = '' #  El consumer de kafka
FORMAT = '' # El formato de datos en Kafka
TOPIC = '' # El nombre del tópico

import faust

# Configuración sencilla de Faust utilizando la configuración importada
app = faust.App(
    COMSUMER,
    broker=BROKER_URL, 
    value_serializer=FORMAT,
)
topic = app.topic(TOPIC)

