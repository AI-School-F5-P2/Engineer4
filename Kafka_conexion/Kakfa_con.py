import faust

# configuracion sencilla de faust
app = faust.App(
    'my-kafka-consumer',
    broker='kafka://localhost:29092',  # Replace with your Kafka broker URL
    value_serializer='json',
    )

# Define a Kafka topic to consume from
topic = app.topic('probando')