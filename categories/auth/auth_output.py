from categories.utils.output import Output


class AuthOutput(Output):
    def show(self, response=''):
        print('Авторизовано!')
