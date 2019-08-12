import unittest
from export_workers.workers.create_file.create_files import create_file
from export_workers.workers.google_drive.google_drive_listener import upload_to_google_drive
from export_workers.workers.send_email.email_listener import job_listener
import pika


CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672))
CHANNEL = CONNECTION.channel()
CHANNEL.queue_declare(queue='answer_to_export')


class CreateFileWorker(unittest.TestCase):
    def test_invalid_job_data(self):
        message = "{'task_id': 787878787, " \
                  "'form_id': 1, 'group_id': [1], " \
                  "'export_format': 'xls'}"

        def callback(channel, method, properties, job_data):
            self.assertEqual(job_data['message'], b'{"task_id": 787878787, "message": {"email": ["Missing data for required field."]}}')
            CHANNEL.stop_consuming()

        create_file("channel", "method", "properties", message)
        CHANNEL.basic_consume(queue='answer_to_export', on_message_callback=callback, auto_ack=True)
        CHANNEL.start_consuming()

    def test_valid_job_data(self):
        message = "{'task_id': 787878787, " \
                  "'form_id': 1, 'group_id': [1], " \
                  "'export_format': 'xls', " \
                  "'email': 'taras.konchak1@gmail.com'}"

        def callback(channel, method, properties, job_data):
            self.assertEqual(job_data, b"{'task_id': 787878787, " \
                                        "'form_id': 1, 'group_id': [1], " \
                                        "'export_format': 'xls', " \
                                        "'email': 'taras.konchak1@gmail.com'}")
            CHANNEL.stop_consuming()

        create_file("channel", "method", "properties", message)
        CHANNEL.basic_consume(queue='upload_on_google_drive', on_message_callback=callback, auto_ack=True)
        CHANNEL.start_consuming()
