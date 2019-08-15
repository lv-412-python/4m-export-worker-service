"""Send requests to services"""
import logging

import requests
from export_workers.create_messages import (create_dict_message,
                                            message_for_queue)


class SendRequest():
    """Send requests to services"""
    def request_to_services(self, url, job_dict):
        """
        Send request to service.
        :param url: str: answer service URL
        :param input_dict: dict: parameters to query
        :return: answers for form.
        """
        try:
            return requests.get(url, params=job_dict,
                                cookies={'session' :job_dict['session'],
                                         'admin': job_dict['admin']})
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
        try:
            url = url + '/{}'.format(job_dict['form_id'])
            return requests.get(url, cookies={'session' :job_dict['session'],
                                              'admin': job_dict['admin']})
        except requests.exceptions.RequestException:
            logging.error("server not responding")
