import requests

from categories.utils.error_handler import parse_error
from categories.utils.extra import *
from categories.utils.output import Output


class Task:
    session = requests.session()
    token = ''
    user_id = ''

    output = Output()

    def __init__(self, settings):
        params = settings.params
        if not len(params):
            return
        self.session = params[0]
        self.token = params[1]
        self.user_id = params[2]

    def run(self):
        pass

    def user_api_request(self, url, **params):
        advanced_methods_initial_api_query = {
            'access_token': self.token,
            'v': '5.103'
        }
        if len(params):
            advanced_methods_initial_api_query = dict_merge(advanced_methods_initial_api_query, params)
            response = wait_for_request(
                lambda: self.session.post(url, params=advanced_methods_initial_api_query)).json()
            error_check = parse_error(response)
            if error_check:
                return ''
            return response
        response = wait_for_request(lambda: self.session.post(url, params=advanced_methods_initial_api_query)).json()
        error_check = parse_error(response)
        if error_check:
            return ''
        return response

    def site_request(self, url, **params):
        if len(params) != 0:
            return wait_for_request(lambda: self.session.post(url, params=params))
        else:
            return wait_for_request(lambda: self.session.post(url))
