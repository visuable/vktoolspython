from categories.settings.settings import Settings


class BotSettings(Settings):
    message = ''
    count = 0
    time = 0

    def __init__(self, params, message, count, time):
        self.params = params
        self.message = message
        self.count = count
        self.time = time
