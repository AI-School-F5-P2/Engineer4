import faust
from decouple import config

# Configuración sencilla de Faust utilizando la configuración importada
app = faust.App(
    config("BROKER_URL"),
    broker=config("COMSUMER"), 
    value_serializer=config("FORMAT"),
)

# Define a Kafka topic to consume from
topic = app.topic(config("TOPIC"))