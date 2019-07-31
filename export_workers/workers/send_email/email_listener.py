"""Processes tasks from 'send_email' queue"""
import logging
from ast import literal_eval

from email_message import Email

from export_workers.create_messages import message_for_queue, create_dict_message
from export_workers.rabbitmq_setup import CHANNEL

EMAIL_SENDER = Email()


def job_listener(channel, method, properties, input_data):
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
        EMAIL_SENDER.send_message(input_dict)
    except ValueError:
        logging.error("invalid input data")
        message = create_dict_message(input_data, "Incorrect input data! Sending failed")
        message_for_queue(message, 'answer_to_export')


CHANNEL.basic_consume(queue='send_email', on_message_callback=job_listener, auto_ack=True)
CHANNEL.start_consuming()
