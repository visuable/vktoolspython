import time

from categories.basic_task import Task
from categories.settings.spammer_settings import SpammerSettings
from categories.utils.constants import WALL_GET, WALL_CREATE_COMMENT


class SpammerTask(Task):
    spammer_settings = SpammerSettings(None, 0, '', 0, 0, 0)

    def __init__(self, spammer_settings):
        self.spammer_settings = spammer_settings
        super(SpammerTask, self).__init__(spammer_settings)

    def run(self):
        posts = self.user_api_request(WALL_GET,
                                      **{'count': '100',
                                         'owner_id': self.spammer_settings.user_id,
                                         }
                                      )
        if self.spammer_settings.primary_count > posts['response']['count']:
            return
        for i in range(self.spammer_settings.primary_count):
            post = posts['response']['items'][i]
            for _ in range(self.spammer_settings.secondary_count):
                result = self.user_api_request(WALL_CREATE_COMMENT, **{
                    'owner_id': post['owner_id'],
                    'post_id': post['id'],
                    'message': self.spammer_settings.message
                })
                time.sleep(self.spammer_settings.interval)
                print(result)
