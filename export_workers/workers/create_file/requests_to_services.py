"""Send requests to services"""
import requests


def request_to_answers_service(url, input_dict):
    """
    Send request to answers service.
    :param url: str: answer service URL
    :param input_dict: dict: parameters to query
    :return: answers for form.
    """
    return requests.get(url, params=input_dict)


def request_to_group_service(url, input_dict):
    """
    Sends request to answers service.
    :param url: groups service URL
    :param input_dict: parameters to query
    :return:
    """
    return requests.get(url, params=input_dict)


def request_to_form_service(url, input_dict):
    """
    Sends request to answers service.
    :param url: form service URL
    :param input_dict: parameters to query
    :return:
    """
    url = url + '/{}'.format(input_dict['form_id'])
    print(requests.get(url))
