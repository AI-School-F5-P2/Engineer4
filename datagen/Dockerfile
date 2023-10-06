FROM python:3.10

WORKDIR /usr/src/app

RUN pip install --no-cache-dir kafka-python Faker

COPY . .

CMD [ "python", "./kafka_push.py" ]