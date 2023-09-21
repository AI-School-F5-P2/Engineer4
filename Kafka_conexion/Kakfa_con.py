import faust

# configuracion sencilla de faust
app = faust.App(
    '',
    broker='',  # Replace with your Kafka broker URL
    value_serializer='',
    )

# Define a Kafka topic to consume from
topic = app.topic('')
