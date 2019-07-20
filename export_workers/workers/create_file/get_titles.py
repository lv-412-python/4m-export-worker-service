"""Get form, groups, fields titles from services"""
import requests

from .requests_to_services import SendRequest
from .serializers.job_schema import FormResponseSchema
from export_workers.workers.config.base_config import Config


class GetTitles():
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
        fields_json = {'field_id': list(fields_id)}
        fields_request = requests.get(Config.FIELD_SERVICE_URL, params=fields_json)
        r_dict = fields_request.json()
        return r_dict

    def get_form_title(self, job_dict):
        response = SendRequest.request_to_form_service(Config.FORM_SERVICE_URL, job_dict)
        response_schema = FormResponseSchema()
        response = response_schema.load(response)
        if response.errors:
            result = ""
        else:
            result = response.data['title']
        return result

