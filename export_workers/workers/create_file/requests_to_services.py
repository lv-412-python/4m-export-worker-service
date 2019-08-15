"""Send requests to services"""
import logging

import requests
from export_workers.create_messages import (create_dict_message,
                                            message_for_queue)


class SendRequest():
    """Send requests to services"""
    def request_to_answer_service(self, url, job_dict):
        """
        Send request to service.
        :param url: str: answer service URL
        :param input_dict: dict: parameters to query
        :return: answers for form.
        """
        parameters = {}
        if job_dict.get('from_date', None):
            parameters['from_date'] = job_dict['from_date']
        if job_dict.get('to_date', None):
            parameters['to_date'] = job_dict['to_date']
        if job_dict['group_id']:
            parameters['group_id'] = job_dict['group_id']
        parameters['form_id'] = job_dict['form_id']
        cookie = {
            'session': job_dict['session'],
            'admin': job_dict['admin']
        }
        try:
            logging.warning(job_dict)
            return requests.get(url, params=parameters, cookies=cookie)
        except requests.exceptions.RequestException:
            logging.error("server not responding")
            message = create_dict_message(job_dict, 'server not responding')
            message_for_queue(message, "answer_to_export")
            return False

    def request_to_fields_service(self, url, fields, job_dict):
        """
        Send request to service.
        :param url: str: service URL
        :param input_dict: dict: parameters to query
        :return: answers for form.
        """
        cookie = {
            'session': job_dict['session'],
            'admin': job_dict['admin']
        }
        try:
            return requests.get(url, params=fields, cookies=cookie)
        except requests.exceptions.RequestException:
            logging.error("server not responding")
            message = create_dict_message(job_dict, 'server not responding')
            message_for_queue(message, "answer_to_export")
            return False


    def request_to_services(self, url, job_dict):
        """
        Send request to service.
        :param url: str:  service URL
        :param input_dict: dict: parameters to query
        :return: answers for form.
        """
        cookie = {
            'session': job_dict['session'],
            'admin': job_dict['admin']
        }
        try:
            return requests.get(url, params=job_dict, cookies=cookie)
        except requests.exceptions.RequestException:
            logging.error("server not responding")
            message = create_dict_message(job_dict, 'server not responding')
            message_for_queue(message, "answer_to_export")
            return False


    def request_to_form_service(self, url, job_dict):
        """
        Sends request to form service.
        :param url: form service URL
        :param job_dict: parameters to query
        :return:
        """
        cookie = {
            'session': job_dict['session'],
            'admin': job_dict['admin']
        }
        try:
            url = url + '/{}'.format(job_dict['form_id'])
            return requests.get(url, cookies=cookie)
        except requests.exceptions.RequestException:
            logging.error("server not responding")
