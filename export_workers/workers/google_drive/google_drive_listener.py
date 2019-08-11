"""Listen queue and upload files to google drive."""
import logging
import os
from ast import literal_eval

from create_drive import DRIVE_SERVICE, GOOGLE_INST

from export_workers.create_messages import message_for_queue, create_dict_message
from export_workers.rabbitmq_setup import CHANNEL

PATH_TO_EXPORT_FILES = os.environ.get('PATH_TO_EXPORT_FILES') + '/'


def upload_to_google_drive(channel, method, properties, job_data):
    """
    Uploads files on google drive and sets permissions to users.
    :param channel: RabbitMQ channel
    :param method: RabbitMQ method
    :param properties: RabbitMq properties
    :param job_data: dict:
    :return:
    """
    try:
        job_data = job_data.decode('utf-8')
        job_data = literal_eval(job_data)
    except TypeError:
        logging.error('invalid job data')
        message = create_dict_message(job_data, "Invalid job_data")
        message_for_queue(message, "answer_to_export")
        return
    file_name = "{}.{}".format(job_data['file_name'], job_data['export_format'])
    files = os.listdir(PATH_TO_EXPORT_FILES)
    if file_name in files:
        file_path = PATH_TO_EXPORT_FILES + file_name
        file_format = 'text/{}'.format(job_data['export_format'])
        url, file_id = GOOGLE_INST.file_to_drive(DRIVE_SERVICE, file_name, file_path, file_format)
        GOOGLE_INST.insert_permission(DRIVE_SERVICE, file_id, job_data['email'], 'user', 'writer')
        job_data.update({'url': url})
        message_for_queue(job_data, 'send_email')
    else:
        logging.warning("file doesn't exist")
        message = create_dict_message(job_data, 'File is not uploaded!')
        message_for_queue(message, "answer_to_export")


CHANNEL.basic_consume(queue='upload_on_google_drive',
                      on_message_callback=upload_to_google_drive, auto_ack=True)
CHANNEL.start_consuming()
