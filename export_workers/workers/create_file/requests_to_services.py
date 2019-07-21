"""Send requests to services"""
import requests

class SendRequest():

    def request_to_services(self, url, job_dict):
        """
        Send request to service.
        :param url: str: answer service URL
        :param input_dict: dict: parameters to query
        :return: answers for form.
        """
        return requests.get(url, params=job_dict)

    def request_to_form_service(self, url, job_dict):
        """
        Sends request to answers service.
        :param url: form service URL
        :param input_dict: parameters to query
        :return:
        """
        url = url + '/{}'.format(job_dict['form_id'])
        print(requests.get(url))
