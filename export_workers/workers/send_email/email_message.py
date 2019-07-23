"""Send email to user"""
import logging
import os
import smtplib
from email.mime.text import MIMEText

from message_templates import EMAIL_TEMPLATE

from export_workers.create_messages import message_for_queue, create_dict_message

EMAIL_ADDRESS = os.environ.get('WORKER_EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('WORKER_EMAIL_PASSWORD')

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_SERVER_PORT = os.environ.get('MAIL_SERVER_PORT')

class Email:
    """Email class"""
    def send_message(self, data):
        """
        Send link to download file with answers.
        :param url: str:url to downloading file
        :param data: dict: Contains receiver email.
        """
        msg = MIMEText(EMAIL_TEMPLATE.format(url=data['url']), 'html')
        msg['Subject'] = 'File with answers for form {}.'.format(data["form_id"])
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = data['email']

        with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_SERVER_PORT) as smtp:
            try:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
                message = create_dict_message(data, "URL for downloading file successfully shipped")
                message_for_queue(message, 'answer_to_export')
            except smtplib.SMTPException:
                logging.error("SMTP server error")
                message = create_dict_message(data, "URL for downloading wasn't shipped!")
                message_for_queue(message, 'answer_to_export')
