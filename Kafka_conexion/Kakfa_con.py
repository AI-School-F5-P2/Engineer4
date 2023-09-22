import faust
from config import *

# Configuración sencilla de Faust utilizando la configuración importada
app = faust.App(
    COMSUMER,
    broker=BROKER_URL, 
    value_serializer=FORMAT,
)

# Define a Kafka topic to consume from
topic = app.topic(TOPIC)
