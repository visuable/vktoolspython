from extra import *


class Task:
    # TODO: проверить методы запросов
    session = None
    token = ''

    def __init__(self, params):
        if not len(params):
            return
        self.session = params[0]
        self.token = params[1]

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
