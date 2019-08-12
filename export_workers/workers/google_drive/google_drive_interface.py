"""Auth class"""
import logging
import os

from apiclient import errors
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    FLAGS = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    FLAGS = None

CREDENTIALS_PATH = os.environ.get('PATH_TO_CREDENTIALS')

class GoogleDriveInterface:
    """Auth class."""
    def __init__(self, scopes, client_secret_file, application_name):
        self.scopes = scopes
        self.client_secret_file = client_secret_file
        self.application_name = application_name


    def get_credentials(self):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        credential_dir = os.path.join(CREDENTIALS_PATH, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'google-drive-credentials.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, self.scopes)
            flow.user_agent = self.application_name
            if FLAGS:
                credentials = tools.run_flow(flow, store, FLAGS)
        return credentials


    def insert_permission(self, service, file_id, value, perm_type, role):
        """Insert a new permission.
        Args:
          service: Drive API service instance.
          file_id: ID of the file to insert permission for.
          value: User or group e-mail address, domain name or None for 'default'
                 type.
          perm_type: The value 'user', 'group', 'domain' or 'default'.
          role: The value 'owner', 'writer' or 'reader'.
        Returns:
          The inserted permission if successful, None otherwise.
        """
        new_permission = {
            'emailAddress': value,
            'type': perm_type,
            'role': role,
            'transferOwnership': True
        }
        response = None
        try:
            response = service.permissions().create(
                fileId=file_id, body=new_permission).execute()
        except errors.HttpError:
            logging.error("permissions wasn't inserted")
        return response


    def file_to_drive(self, drive_service, filename, filepath, mimetype):
        """
        Uploads file to google drive
        :param drive_service: drive to upload files
        :param filename: str: name of the file.
        :param filepath: str: path to file.
        :param mimetype: type of the file.
        :return: list: list of 2 elements. 1 - link for downloading
        2 - id file on google drive.
        """
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath,
                                mimetype=mimetype)
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id, webContentLink').execute()
        link_for_downloading = file.get('webContentLink')
        file_id = file.get('id')
        return [link_for_downloading, file_id]
