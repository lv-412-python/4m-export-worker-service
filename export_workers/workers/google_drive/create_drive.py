"""Create drive_service for connection to google drive."""
import httplib2
from apiclient import discovery
from google_drive_interface import GoogleDriveInterface

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = '4M-EXPORT-SERVICE'
GOOGLE_INST = GoogleDriveInterface(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
CREDENTIALS = GOOGLE_INST.get_credentials()

HTTP = CREDENTIALS.authorize(httplib2.Http())
DRIVE_SERVICE = discovery.build('drive', 'v3', http=HTTP)
