import faust

CONSUMER = "my-kafka-consumer"
BROKER_URL = "kafka://localhost:29092"
FORMAT = "json"
TOPIC = "probando"

app = faust.App(
    CONSUMER,
    broker=BROKER_URL, 
    value_serializer=FORMAT,
)

topic = app.topic(TOPIC)

