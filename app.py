import os
from flask import Flask, request
import pika

# RabbitMQ constants
RABBITMQ_CONNECTION_STRING = os.getenv('RABBITMQ_CONNECTION_STRING', 'localhost')
RABBITMQ_EXCAHNGE = 'service_callbacks'

# Application
app = Flask(__name__)


@app.route('/webhooks/todoist/', methods=['GET', 'POST'])
def todoist_webhook():
    if request.method == 'POST':
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_CONNECTION_STRING))
        channel = connection.channel()
        channel.exchange_declare(exchange=RABBITMQ_EXCAHNGE, exchange_type='topic')

        channel.basic_publish(exchange=RABBITMQ_EXCAHNGE,
                              routing_key='todoist',
                              body=request.data,
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))
        connection.close()

    return 'ok'


@app.route('/webhooks/trello/', methods=['GET', 'POST', 'HEAD'])
def trello_webhook():
    if request.method == 'POST':
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_CONNECTION_STRING))
        channel = connection.channel()
        channel.exchange_declare(exchange=RABBITMQ_EXCAHNGE, exchange_type='topic')

        channel.basic_publish(exchange=RABBITMQ_EXCAHNGE,
                              routing_key='trello',
                              body=request.data,
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))
        connection.close()

    return 'ok'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
