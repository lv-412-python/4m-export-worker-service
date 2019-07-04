"""Processes tasks from 'send_email' queue"""
from ast import literal_eval
import pika
from url import create_url
from email_message import send_message


CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='send_email')
CHANNEL.queue_declare(queue='export_answer')


def callback(channel, method, properties, request):
    # pylint: disable=unused-argument
    """
    Callback starts executing when appears task for processing in queue
    :param method: method
    :param properties: properties
    :param request: str: Dictionary with keys (form_id, groups, format) converted to string
    :return: str: Message with status to export service
    """
    try:
        request = request.decode('utf-8')
        data = literal_eval(request)
        url_for_file = create_url(data)
        send_message(url_for_file, data)
    except ValueError:
        CHANNEL.basic_publish(exchange='', routing_key='export_answer', \
                              body='Incorrect input data! Sending failed!')


CHANNEL.basic_consume(queue='send_email', on_message_callback=callback, auto_ack=True)
CHANNEL.start_consuming()
