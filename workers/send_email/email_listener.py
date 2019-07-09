"""Processes tasks from 'send_email' queue"""
import os
from ast import literal_eval

from email_message import send_message
from export_worker_service.create_messages import message_for_queue, create_dict_message
from export_worker_service.rabbitmq_setup import CHANNEL

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')


def send_email(channel, method, properties, input_data):
    # pylint: disable=unused-argument
    """
    Callback starts executing when appears task for processing in queue
    :param method: method
    :param properties: properties
    :param input_data: str: Dictionary with keys (form_id, groups, format) converted to string
    :return: str: Message with status to export service
    """
    try:
        input_data = input_data.decode('utf-8')
        input_dict = literal_eval(input_data)
        send_message(input_dict)
    except ValueError:
        message = create_dict_message(input_data, "Incorrect input data! Sending failed")
        message_for_queue(message, 'answer_to_export')
        return

CHANNEL.basic_consume(queue='send_email', on_message_callback=send_email, auto_ack=True)
CHANNEL.start_consuming()
