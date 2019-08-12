"""Get form, groups, fields titles from services"""
import logging
from requests_to_services import SendRequest
from export_workers.workers.config.base_config import Config

SENDER = SendRequest()

class GetTitles():
    """Class that get titles by ID"""
    def get_field_title(self, result):
        """changes field_id to field_title
        :param result: list: result of sqlalchemy query
        :return r_dict: dict: key - field_id, value - field_title
        """
        # creates set of fields_id
        fields_id = set()
        for i, _ in enumerate(result):
            field = result[i]["field_id"]
            fields_id.add(int(field))
        # request titles based on needed fields_id
        fields_params = {'field_id': list(fields_id)}
        fields_request = SENDER.request_to_services(Config.FIELD_SERVICE_URL, fields_params)
        result_dict = {}
        if not fields_request:
            for field_id in fields_id:
                result_dict.update({field_id: "Title"})
            return result_dict
        r_dict = fields_request.json()
        for dict_title in r_dict:
            result_dict.update({dict_title['id']: dict_title['title']})
        return result_dict

    def get_form_title(self, response):
        """
        Get form title by ID
        :param response: response from form_service
        :return: form title
        """
        try:
            data = response.json()
            title = data['title']
        except AttributeError:
            logging.error("invalid input data")
            title = 'Title'
        return title

    def get_group_titles(self, response):
        """
        Get group titles by ID
        :param response: response from groups_service
        :return: list: list of titles
        """
        try:
            data = response.json()
            group_titles = []
            for group in data:
                group_titles.append(group['title'])
        except AttributeError:
            logging.error("invalid input data")
            group_titles = []
        return group_titles
