"""Creates RabbitMQ channel, and queues."""
import pika

CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq", port=5672))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='export')
CHANNEL.queue_declare(queue='send_email')
CHANNEL.queue_declare(queue='answer_to_export')
CHANNEL.queue_declare(queue='upload_on_google_drive')
