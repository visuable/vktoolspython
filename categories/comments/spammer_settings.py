from categories.settings import Settings


class SpammerSettings(Settings):
    interval = 0
    message = ''
    count = 0
    user_id = 0

    def __init__(self, params, interval, message, count, user_id):
        self.params = params
        self.interval = interval
        self.message = message
        self.count = count
        self.user_id = user_id
