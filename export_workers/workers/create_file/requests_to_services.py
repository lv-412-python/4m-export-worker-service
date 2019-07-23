"""Send requests to services"""
import logging
import urllib.error

import requests


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
            return requests.get(url, params=job_dict)
        except urllib.error.HTTPError:
            logging.error("server not responding")


    def request_to_form_service(self, url, job_dict):
        """
        Sends request to form service.
        :param url: form service URL
        :param job_dict: parameters to query
        :return:
        """
        try:
            url = url + '/{}'.format(job_dict['form_id'])
            return requests.get(url)
        except urllib.error.HTTPError:
            logging.error("server not responding")
