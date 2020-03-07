import requests

from extra import *


class Task:
    # TODO: проверить методы запросов
    session = requests.Session()
    token = ''

    def __init__(self, settings):
        if not len(settings.params):
            return
        self.session = settings.params[0]
        self.token = settings.params[1]

    def run(self):
        pass

    def user_api_request(self, url, **params):
        advanced_methods_initial_api_query = {
            'access_token': self.token,
            'v': '5.103'
        }
        if len(params):
            advanced_methods_initial_api_query = dict_merge(advanced_methods_initial_api_query, params)
            return wait_for_request(lambda: self.session.post(url, params=advanced_methods_initial_api_query))
        return wait_for_request(lambda: self.session.post(url, params=advanced_methods_initial_api_query))

    def site_request(self, url, **params):
        if len(params) != 0:
            return wait_for_request(lambda: self.session.post(url, params=params))
        return wait_for_request(lambda: self.session.post(url))
