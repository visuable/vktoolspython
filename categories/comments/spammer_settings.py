from categories.settings import Settings


class SpammerSettings(Settings):
    __interval__ = 0
    __message__ = ''
    __count__ = 0
    __user_id__ = 0

    def __init__(self, params, interval, message, count, user_id):
        self.__params__ = params
        self.__interval__ = interval
        self.__message__ = message
        self.__count__ = count
        self.__user_id__ = user_id
