"""Create drive_service for connection to google drive."""
from __future__ import print_function

import httplib2
from apiclient import discovery
from auth import Auth

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = '4M-EXPORT-SERVICE'
AUTH_INSTANCE = Auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
CREDENTIALS = AUTH_INSTANCE.get_credentials()

HTTP = CREDENTIALS.authorize(httplib2.Http())
DRIVE_SERVICE = discovery.build('drive', 'v3', http=HTTP)
