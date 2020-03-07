from categories.settings import Settings


class BotSettings(Settings):
    __message__ = ''
    __count__ = 0

    def __init(self, params, message, count):
        self.__params__ = params
        self.__message__ = message
        self.__count__ = count
