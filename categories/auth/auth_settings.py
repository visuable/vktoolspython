from categories.settings import Settings


class AuthSettings(Settings):
    __login__ = ''
    __password__ = ''

    def __init__(self, login, password):
        self.__login__ = login
        self.__password__ = password
