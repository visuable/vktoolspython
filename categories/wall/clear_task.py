import time

from loguru import logger

from categories.basic_task import Task


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
                logger.success('Все записи удалены')
                return
            logger.trace('Список идентификаторов постов извлечен')
            responses = []
            # Запрос на удаление поста
            for identifier in ids:
                payload = {'post_id': identifier}
                responses.append(self.__wall_delete_request(payload))
                logger.success('Пост удален')
            time.sleep(3)

    def __wall_delete_request(self, payload):
        return self.user_api_request('https://api.vk.com/method/wall.delete', **payload)

    def __wall_get_request(self):
        response = self.user_api_request('https://api.vk.com/method/wall.get').json()
        return response
