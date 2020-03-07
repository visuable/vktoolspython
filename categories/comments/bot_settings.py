from categories.settings import Settings


class BotSettings(Settings):
    message = ''
    count = 0

    def __init(self, params, message, count):
        self.params = params
        self.message = message
        self.count = count
