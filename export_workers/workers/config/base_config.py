"""Config file."""
import os

PORT = os.environ.get('SERVICES_PORT')

class Config:
    """Config class"""
    ANSWERS_SERVICE_URL = "http://answers-service:{0}/answers".format(PORT)
    GROUP_SERVICE_URL = "http://groups-service:{0}/group".format(PORT)
    FIELD_SERVICE_URL = "http://fields-service:{0}/field".format(PORT)
    FORM_SERVICE_URL = "http://forms-service:{0}/form".format(PORT)
