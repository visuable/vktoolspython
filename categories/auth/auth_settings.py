from categories.settings.settings import Settings


class AuthSettings(Settings):
    login = ''
    password = ''

    def __init__(self, login, password):
        self.login = login
        self.password = password
