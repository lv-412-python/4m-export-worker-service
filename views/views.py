"Route to download file"
import os
import urllib.parse
from flask import send_file
from create_app import APP
from create_file.files import file_name
from delete_files import PATH




@APP.route('/download/<file>')
def download(file):
    """
    Send file if it's exist.
    :param file: url to file
    :return: send file to user
    """
    files = os.listdir(PATH)
    request = dict(urllib.parse.parse_qsl(file))
    name = "{}.{}".format(file_name(request), request['format'])
    if name in files:
        response = send_file(PATH + '/' + name)
    else:
        response = "Sorry, we don't have this file! =)"
    return response
