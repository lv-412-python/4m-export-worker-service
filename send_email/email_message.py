"""Send email to user"""
import smtplib
from email.mime.text import MIMEText
from url import EMAIL_TEMPLATE
EMAIL_ADDRESS = '4m.export.service@gmail.com'
EMAIL_PASSWORD = 'qwertyytrewq13242151'



def send_message(url, data):
    """
    Send link to download file with answers.
    :param url: str:url to downloading file
    :param data: dict: Contains receiver email.
    """
    msg = MIMEText(EMAIL_TEMPLATE.format(url=url), 'html')
    msg['Subject'] = 'File with answers for form {}.'.format(data["form_id"])
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'taras.konchak1@gmail.com'
    # msg['To'] = data['email']

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
