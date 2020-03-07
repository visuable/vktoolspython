from lxml import etree

from categories.auth.auth_settings import AuthSettings
from categories.basic_task import Task
from constants import OAUTH_AUTH, REDIRECT_URI, VK_MOBILE, CLIENT_ID, RESPONSE_TYPE, SCOPE, REVOKE
from extra import parse_token


class AuthTask(Task):
    auth_settings = AuthSettings('', '')

    def __init__(self, auth_settings):
        self.auth_settings = auth_settings

    def run(self):
        authorization_response = self.__http_authorize()
        # Если прошла авторизация, то остался список cookie-файлов вк
        if authorization_response.cookies:
            oauth_token_response_url = self.__get_token_request()
            try:
                token_string = parse_token(oauth_token_response_url)
                # Возращаем кортеж, состоящий из сессии и токена для выполнения запросов к API
                return self.session, token_string
            except Exception:
                pass
        return False

    def __get_token_request(self):
        oauth_token_response_url = self.site_request(OAUTH_AUTH,
                                                     response_type=RESPONSE_TYPE, client_id=CLIENT_ID,
                                                     redirect_uri=REDIRECT_URI,
                                                     revoke=REVOKE, scope=SCOPE
                                                     ).url
        return oauth_token_response_url

    def __http_authorize(self):
        # Запрос на получение HTML формы с мобильной версии сайта
        # Это необходимо, чтобы получить аттрибут action, в котором содержится адрес
        # Через который следует передать пароль и логин
        vk_mobile_html_form_response_text = self.site_request(VK_MOBILE).text
        # Извлечение этого аттрибута через XPath
        xpath_parser = etree.HTML(vk_mobile_html_form_response_text)
        action_string = xpath_parser.xpath('//form')[0].attrib['action']
        # Параметры на запрос авторизации
        authorization_response = self.site_request(action_string, **{
            'email': self.auth_settings.login,
            'pass': self.auth_settings.password
        }
                                                   )
        return authorization_response
