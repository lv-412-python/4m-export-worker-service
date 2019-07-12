"""Functions to create messages"""
import json

from export_worker_service.rabbitmq_setup import CHANNEL


def create_dict_message(job_dict, message):
    """
    Creates dict for the message.
    :param job_dict: dict: Data about job.
    :param message: str: Message with result of operation.
    :return:
    """
    result = {
        'id': job_dict['id'],
        'message': message
    }
    return result


def message_for_queue(message, queue):
    """
    Send message with status of operation.
    :param message: dict: Dict with job data.
    :param queue: Name of the queue.
    :return: None
    """
    CHANNEL.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
