from categories.settings import Settings


class SpammerSettings(Settings):
    interval = 0
    message = ''
    primary_count = 0
    secondary_count = 0
    user_id = 0

    def __init__(self, params, interval, message, primary_count, secondary_count, user_id):
        self.params = params
        self.interval = interval
        self.message = message
        self.primary_count = primary_count
        self.secondary_count = secondary_count
        self.user_id = user_id
