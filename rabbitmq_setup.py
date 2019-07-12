"""Creates RabbitMQ channel, and queues."""
import os

import pika

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')

CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='export')
CHANNEL.queue_declare(queue='send_email')
CHANNEL.queue_declare(queue='answer_to_export')
CHANNEL.queue_declare(queue='upload_on_google_drive')
