import faust

CONSUMER = ""
BROKER_URL = ""
FORMAT = ""
TOPIC = ""

app = faust.App(
    CONSUMER,
    broker=BROKER_URL, 
    value_serializer=FORMAT,
)

topic = app.topic(TOPIC)

