import unittest

from export_workers.workers.google_drive.google_drive_listener import upload_to_google_drive
import pika

CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='answer_to_export')


class CreateFileWorker(unittest.TestCase):

    def test_invalid_job_data(self):
        message = "{'task_id': 787878787, " \
                  "'form_id': 1, 'group_id': [1], " \
                  "'export_format': xls'asdasd:a " \
                  "'email': 'taras.konchak1@gmail.com'}"

        def callback(channel, method, properties, job_data):
            self.assertEqual(job_data, b"Invalid job_data")
            CHANNEL.stop_consuming()

        upload_to_google_drive("channel", "method", "properties", message)
        CHANNEL.basic_consume(queue='answer_to_export', on_message_callback=callback, auto_ack=True)
        CHANNEL.start_consuming()

    def test_nonexistent_file(self):
        message = "{'task_id': 787878787, " \
                  "'form_id': 1, 'group_id': [1], " \
                  "'export_format': 'xls', " \
                  "'email': 'taras.konchak1@gmail.com', }" \
                  "'file_name': 'test'"


        def callback(channel, method, properties, job_data):
            self.assertEqual(job_data["message"], b"'File is not uploaded!'")
            CHANNEL.stop_consuming()

        upload_to_google_drive("channel", "method", "properties", message)
        CHANNEL.basic_consume(queue='answer_to_export', on_message_callback=callback, auto_ack=True)
        CHANNEL.start_consuming()

