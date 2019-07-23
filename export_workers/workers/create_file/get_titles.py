"""Get form, groups, fields titles from services"""
import requests
import logging
from requests_to_services import SendRequest
from export_workers.workers.config.base_config import Config

SENDER = SendRequest()

class GetTitles():
    def get_field_title(self, result):
        """changes field_id to field_title
        :param result: list: result of sqlalchemy query
        :return r_dict: dict: key - field_id, value - field_title
        """
        # creates set of fields_id
        print(12)
        fields_id = set()
        for i, _ in enumerate(result):
            field = result[i]["field_id"]
            fields_id.add(int(field))
        # request titles based on needed fields_id
        fields_params = {'field_id': list(fields_id)}
        fields_request = SENDER.request_to_services(Config.FIELD_SERVICE_URL, fields_params)
        r_dict = fields_request.json()
        result_dict = {}
        for dict_title in r_dict:
            result_dict.update({dict_title['id']: dict_title['title']})
        return result_dict

    def get_form_title(self, response):
        try:
            data = response.json()
            title = data['title']
        except AttributeError:
            title = 'Title'
        return title

    def get_group_titles(self, response):
        try:
            data = response.json()
            group_titles = []
            for group in data:
                group_titles.append(group['title'])
        except AttributeError:
            group_titles = []
        return group_titles
