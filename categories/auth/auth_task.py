import requests
from loguru import logger
from lxml import etree

from categories.basic_task import Task
from extra import parse_token


class AuthTask(Task):
    __login = ''
    __password = ''

    def __init__(self, login, password):
        self.__login = login
        self.__password = password
        self.session = requests.session()

    def run(self):
        authorization_response = self.__http_authorize()
        # Если прошла авторизация, то остался список cookie-файлов сайта
        if authorization_response.cookies:
            logger.info('Успешно авторизовано')
            # TODO: спрятать client_id
            oauth_token_response_url = self.__get_token_request()
            try:
                token_string = parse_token(oauth_token_response_url)
                logger.info('Токен распознан')
                # Возращаем кортеж, состоящий из сессии и токена для выполнения запросов к API
                return self.session, token_string
            except Exception:
                pass
        return False

    def __get_token_request(self):
        oauth_token_response_url = self.site_request('https://oauth.vk.com/authorize',
                                                     response_type='token', client_id='7203136',
                                                     redirect_uri='https://oauth.vk.com/blank.html',
                                                     revoke='0', scope='wall'
                                                     ).url
        logger.trace('URL, содержащий токен получен')
        return oauth_token_response_url

    def __http_authorize(self):
        # Запрос на получение HTML формы с мобильной версии сайта
        # Это необходимо, чтобы получить аттрибут action, в котором содержится адрес
        # Через который следует передать пароль и логин
        vk_mobile_html_form_response_text = self.site_request('https://m.vk.com').text
        # Извлечение этого аттрибута через XPath
        xpath_parser = etree.HTML(vk_mobile_html_form_response_text)
        action_string = xpath_parser.xpath('//form')[0].attrib['action']
        logger.trace('URL для авторизации получен')
        # Параметры на запрос авторизации
        authorization_response = self.site_request(action_string, **{
            'email': self.__login,
            'pass': self.__password
        }
                                                   )
        return authorization_response
