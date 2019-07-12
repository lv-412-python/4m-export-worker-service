"""Uploads file to google drive."""
# pylint: disable=import-error
from apiclient.http import MediaFileUpload
from drive import DRIVE_SERVICE


def upload_file_to_drive(filename, filepath, mimetype):
    # pylint: disable=no-member
    """
    Uploads file to google drive
    :param filename: str: name of the file.
    :param filepath: str: path to file.
    :param mimetype: type of the file.
    :return: list: list of 2 elements. 1 - link for downloading
    2 - id file on google drive.
    """
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = DRIVE_SERVICE.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id, webContentLink').execute()
    link_for_downloading = file.get('webContentLink')
    file_id = file.get('id')
    return [link_for_downloading, file_id]
