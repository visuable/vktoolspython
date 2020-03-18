from lxml import etree

from categories.auth.auth_settings import AuthSettings
from categories.basic_task import Task
from categories.utils.constants import OAUTH_AUTH, REDIRECT_URI, VK_MOBILE, CLIENT_ID, RESPONSE_TYPE, SCOPE, REVOKE, \
    VERSION, STATE, \
    USERS_GET
from categories.utils.extra import parse_token


class AuthTask(Task):
    auth_settings = AuthSettings('', '')

    def __init__(self, auth_settings):
        self.auth_settings = auth_settings
        super(AuthTask, self).__init__(auth_settings)

    def run(self):
        authorization_response = self.__http_authorize()
        # Если прошла авторизация, то остался список cookie-файлов вк
        if authorization_response.cookies:
            oauth_token_response_url = self.__get_token_request()
            token_string = parse_token(oauth_token_response_url)
            if token_string is None:
                return oauth_token_response_url
            # Возращаем кортеж, состоящий из сессии, токена
            # и идентификатора текущего пользователя для выполнения запросов к API
            self.token = token_string
            # Получение id текущего пользователя
            user_id = self.user_api_request(USERS_GET)['response'][0]['id']
            return self.session, self.token, user_id

    def __get_token_request(self):
        # Запрос на получение токена
        oauth_token_response_url = self.site_request(OAUTH_AUTH,
                                                     response_type=RESPONSE_TYPE, client_id=CLIENT_ID,
                                                     redirect_uri=REDIRECT_URI,
                                                     revoke=REVOKE, scope=SCOPE,
                                                     v=VERSION, state=STATE
                                                     )
        return oauth_token_response_url.url

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
