import requests

from categories.utils.extra import *


class Task:
    session = requests.session()
    token = ''
    user_id = ''

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
            return wait_for_request(lambda: self.session.post(url, params=advanced_methods_initial_api_query)).json()
        return wait_for_request(lambda: self.session.post(url, params=advanced_methods_initial_api_query)).json()

    def site_request(self, url, request_type='POST', **params):
        if len(params) != 0:
            if request_type == 'GET':
                return wait_for_request(lambda: self.session.get(url, params=params))
            if request_type == 'POST':
                return wait_for_request(lambda: self.session.post(url, params=params))
            else:
                return False
        else:
            if request_type == 'GET':
                return wait_for_request(lambda: self.session.get(url))
            if request_type == 'POST':
                return wait_for_request(lambda: self.session.post(url))
