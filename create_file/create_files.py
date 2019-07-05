"""Creates csv, pdf, xls files"""
from ast import literal_eval
import pika
import requests
from config.base_config import Config
from models.answers import Answer
from files import FILE_MAKERS, file_name
from db import SESSION
from serializers.answer_schema import ANSWERS_SCHEMA
from sqlalchemy.exc import OperationalError

CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='export')
CHANNEL.queue_declare(queue='send_email')
CHANNEL.queue_declare(queue='answer_to_export')


def message_for_queue(message, queue):
    """Send message with status of operation"""
    CHANNEL.basic_publish(exchange='', routing_key=queue, body=message)

def get_field_title_by_id(result):
    """changes field_id to field_title
    :param result: list: result of sqlalchemy query
    :return dict
    """
    # creates set of fields_id
    fields_id = set()
    for i, _ in enumerate(result):
        field = result[i]["field_id"]
        fields_id.add(int(field))
    # request titles based on needed fields_id
    fields_json = {'fields': list(fields_id)}
    fields_request = requests.get(Config.FIELD_SERVICE_URL, json=fields_json)
    r_dict = fields_request.json()
    return r_dict

def get_answers_for_form(form, groups):
    """
    Gets users responses from the database
    :param form: int : Form ID
    :param groups: list : List of group, if groups is []
    returns answers for entire form.
    :return: dictionary : Returns dictionary.
    Keys are user, values are dictionaries
    with field and reply for this field.
    """
    answers = []
    try:
        if groups:
            for group in groups:
                answers += SESSION.query(Answer).filter_by(form_id=form, group_id=group).all()
        else:
            answers = SESSION.query(Answer).filter_by(form_id=form).all()
    except OperationalError:
        message_for_queue("db error", "answer_to_export")
    list_of_answers = ANSWERS_SCHEMA.dump(answers).data
    field_title = get_field_title_by_id(list_of_answers)
    users_answers = {answer.user_id: {} for answer in answers}
    for answer in answers:
        title = field_title[str(answer.field_id)]
        users_answers[answer.user_id][title] = answer.reply
    if not users_answers:
        users_answers = {}
    return users_answers


def create_file(channel, method, properties, job):
    # pylint: disable=unused-argument
    """
    Callback starts executing when appears task for processing in queue
    :param method: method
    :param properties: properties
    :param request: str: Dictionary with keys (form_id, groups, format) converted to string
    :param
    :return: str: Message with status to export service
    """
    job = job.decode('utf-8')
    data = literal_eval(job)
    answers = get_answers_for_form(data["form_id"], data['groups'])
    if answers:
        name = file_name(data)
        format_ = data['format']
        if format_ in FILE_MAKERS.keys():
            FILE_MAKERS[format_](answers, name)
            message_for_queue(job, 'send_email')
            message = ["File successfully sended!", 'answer_to_export']
        else:
            message = ["Can't write file in this format!", 'answer_to_export']
    else:
        message = ["Answers don't exist!", 'answer_to_export']
    return message_for_queue(message[0], message[1])


CHANNEL.basic_consume(queue='export', on_message_callback=create_file, auto_ack=True)
CHANNEL.start_consuming()
