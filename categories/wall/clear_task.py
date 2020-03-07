import time

from categories.basic_task import Task
from constants import WALL_DELETE, WALL_GET


class WallCleanerTask(Task):

    def __init__(self, settings):
        super(WallCleanerTask, self).__init__(settings)

    def run(self):
        # Запрос на получение всех постов со стены
        while True:
            response = self.__wall_get_request()
            ids = []
            # Перебор элементов
            for element in response['response']['items']:
                ids.append(element['id'])
            if not ids:
                return
            responses = []
            # Запрос на удаление поста
            for identifier in ids:
                payload = {'post_id': identifier}
                responses.append(self.__wall_delete_request(payload))
            time.sleep(3)

    def __wall_delete_request(self, payload):
        return self.user_api_request(WALL_DELETE, **payload)

    def __wall_get_request(self):
        response = self.user_api_request(WALL_GET).json()
        return response
