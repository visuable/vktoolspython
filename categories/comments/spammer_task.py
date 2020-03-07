from categories.basic_task import Task
from categories.comments.spammer_settings import SpammerSettings


class SpammerTask(Task):
    spammer_settings = SpammerSettings(None, 0, '', 0, 0)

    def __init__(self, spammer_settings):
        self.spammer_settings = spammer_settings
        super(SpammerTask, self).__init__(spammer_settings)
