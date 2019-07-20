"""Creates csv, pdf, xls files"""
from ast import literal_eval
from export_workers.create_messages import (
    create_dict_message,
    message_for_queue
)

from export_workers.rabbitmq_setup import CHANNEL
from files import (
    xls_file,
    csv_file,
    pdf_file,
    create_file_name
)
from get_titles import get_field_title_by_id
from requests_to_services import (
    request_to_answers_service,
    # request_to_group_service
)

from serializers.job_schema import JobSchema
from export_workers.workers.config.base_config import Config


FILE_MAKERS = {
    'xls': xls_file,
    'csv': csv_file,
    'pdf': pdf_file
}


def get_answers_for_form(answers):
    """
    Gets users responses from the database
    :param answers: answers
    returns answers for entire form.
    :return: dictionary : Returns dictionary.
    Keys are user, values are dictionaries
    with field and reply for this field.
    """
    answers_list = literal_eval(answers.text)
    print(answers_list)
    users_answers = {answer['user_id']: {} for answer in answers_list}
    field_title = get_field_title_by_id(answers.json())
    for answer in answers_list:
        title = field_title[str(answer['field_id'])]
        users_answers[answer['user_id']][title] = answer['reply']
    return users_answers


def create_file(channel, method, properties, job_data):
    # pylint: disable=unused-argument
    """
    Callback starts executing when appears task for processing in queue
    :param method: method
    :param properties: properties
    :param job_data: str: Dictionary with keys (form_id, groups, format) converted to string
    :param
    :return: str: Message with status to export service
    """
    print(job_data)
    job_data = job_data.decode('utf-8')
    job_dict = literal_eval(job_data)
    job_schema = JobSchema()
    job_dict = job_schema.load(job_dict)
    if job_dict.errors:
        message = create_dict_message(job_dict.data, job_dict.errors)
        message_for_queue(message, 'answer_to_export')
        return
    job_dict = job_dict.data
    answers = request_to_answers_service(Config.ANSWERS_SERVICE_URL, job_dict)
    if not answers:
        message = create_dict_message(job_dict, "Answers does not exist")
        message_for_queue(message, "answer_to_export")
        return
    answers = get_answers_for_form(answers)
    # groups_title = request_to_group_service(Config.GROUP_SERVICE_URL, job_dict)
    # form_title = request_to_form_service(Config.FORM_SERVICE_URL, job_dict)
    # name = file_name(groups_title, form_title)
    file_name = create_file_name(job_dict)
    export_format = job_dict['export_format']
    status = FILE_MAKERS[export_format](answers, file_name)
    if not status:
        message = create_dict_message(job_dict, 'Something went wrong! File is not created!')
        message_for_queue(message, "answer_to_export")
        return
    job_dict.update({'file_name': file_name})
    message_for_queue(job_dict, 'upload_on_google_drive')

print(123123123123123123131231231231313123123123123131231231231232131231)
CHANNEL.basic_consume(queue='export', on_message_callback=create_file, auto_ack=True)
CHANNEL.start_consuming()
