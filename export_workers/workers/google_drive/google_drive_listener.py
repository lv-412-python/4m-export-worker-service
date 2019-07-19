"""Listen queue and upload files to google drive."""
import os
from ast import literal_eval

from drive import DRIVE_SERVICE
from export_workers.create_messages import message_for_queue, create_dict_message
from export_workers.rabbitmq_setup import CHANNEL
from set_permissions import insert_permission
from upload_file import upload_file_to_drive

PATH_TO_EXPORT_FILES = os.environ.get('PATH_TO_EXPORT_FILES') + '/'
print(123123123123123)

def upload_to_google_drive(channel, method, properties, job_data):
    # pylint: disable=unused-argument
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
    except TypeError as error:
        print(error)
        return
    file_name = "{}.{}".format(job_data['file_name'], job_data['export_format'])
    files = os.listdir(PATH_TO_EXPORT_FILES)
    if file_name in files:
        file_path = PATH_TO_EXPORT_FILES + file_name
        file_format = 'text/{}'.format(job_data['export_format'])
        url_for_downloading, file_id = upload_file_to_drive(file_name, file_path, file_format)
        insert_permission(DRIVE_SERVICE, file_id, job_data['email'], 'user', 'writer')
        job_data.update({'url': url_for_downloading})
        message_for_queue(job_data, 'send_email')
    else:
        message = create_dict_message(job_data, 'File is not uploaded!')
        message_for_queue(message, "answer_to_export")


CHANNEL.basic_consume(queue='upload_on_google_drive',
                      on_message_callback=upload_to_google_drive, auto_ack=True)
CHANNEL.start_consuming()
