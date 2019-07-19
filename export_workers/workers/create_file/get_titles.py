"""Get form, groups, fields titles from services"""
import requests

from export_workers.workers.config.base_config import Config


def get_field_title_by_id(result):
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
