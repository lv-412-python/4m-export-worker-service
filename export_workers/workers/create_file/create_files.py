"""Creates csv, pdf, xls files"""
import logging
from ast import literal_eval
from logging.config import fileConfig

from files import (
    xls_file,
    csv_file,
    pdf_file,
    create_file_name
)
from get_titles import GetTitles
from requests_to_services import SendRequest
from serializers.job_schema import JobSchema

from export_workers.create_messages import (
    create_dict_message,
    message_for_queue
)
from export_workers.rabbitmq_setup import CHANNEL
from export_workers.workers.config.base_config import Config
# pylint: disable=unused-import
import export_workers.delete_files

fileConfig('logging.config')

FILE_MAKERS = {
    'xls': xls_file,
    'csv': csv_file,
    'pdf': pdf_file
}

GET_TITLE = GetTitles()
SENDER = SendRequest()
JOB_SCHEMA = JobSchema()


def get_answers_for_form(response, job_dict):
    """
    Gets users responses from the database
    :param response: response from answers service
    returns answers for entire form.
    :return: dictionary : Returns dictionary.
    Keys are user, values are dictionaries
    with field and reply for this field.
    """
    answers_list = response.json()
    users_answers = {answer['user_id']: {} for answer in answers_list}
    field_title = GET_TITLE.get_field_title(answers_list, job_dict)
    for answer in answers_list:
        title = field_title[answer['field_id']]
        users_answers[answer['user_id']][title] = answer['reply']
    return users_answers


def create_file(channel, method, properties, job_data):
    """
    Callback starts executing when appears task for processing in queue
    :param method: method
    :param properties: properties
    :param job_data: str: Dictionary with keys (form_id, groups, format) converted to string
    :param
    :return: str: Message with status to export service
    """
    job_data = job_data.decode('utf-8')
    job_dict = literal_eval(job_data)
    job_dict = JOB_SCHEMA.load(job_dict)
    if job_dict.errors:
        message = create_dict_message(job_dict.data, job_dict.errors)
        message_for_queue(message, 'answer_to_export')
        logging.warning("invalid input data")
        return
    job_dict = job_dict.data
    response = SENDER.request_to_answer_service(Config.ANSWERS_SERVICE_URL, job_dict)
    if not response:
        return
    answers = get_answers_for_form(response, job_dict)
    if job_dict['group_id']:
        group_response = SENDER.request_to_services(Config.GROUP_SERVICE_URL, job_dict)
        groups_title = GET_TITLE.get_group_titles(group_response)
    else:
        groups_title = ''
    forms_response = SENDER.request_to_form_service(Config.FORM_SERVICE_URL, job_dict)
    form_title = GET_TITLE.get_form_title(forms_response)
    file_name = create_file_name(form_title, groups_title)
    export_format = job_dict['export_format']
    status = FILE_MAKERS[export_format](answers, file_name)
    if not status:
        message = create_dict_message(job_dict, 'Something went wrong! File is not created!')
        message_for_queue(message, "answer_to_export")
        logging.warning("file didn't created")
        return
    job_dict.update({'file_name': file_name})
    message_for_queue(job_dict, 'upload_on_google_drive')


CHANNEL.basic_consume(queue='export', on_message_callback=create_file, auto_ack=True)
CHANNEL.start_consuming()
