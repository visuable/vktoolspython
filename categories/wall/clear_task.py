from loguru import logger

from categories.basic_task import Task


class WallCleanerTask(Task):

    def run(self):
        # Запрос на получение всех постов со стены
        response = self.__wall_get_request()
        ids = []
        # Перебор элементов
        for element in response['response']['items']:
            ids.append(element['id'])
        logger.trace('Список идентификаторов постов извлечен')
        responses = []
        # Запрос на удаление поста
        for identifier in ids:
            payload = {'post_id': identifier}
            responses.append(self.__wall_delete_request(payload))
            logger.success('Пост удален')
        return responses

    def __wall_delete_request(self, payload):
        return self.user_api_request('https://api.vk.com/method/wall.delete', **payload)

    def __wall_get_request(self):
        response = self.user_api_request('https://api.vk.com/method/wall.get').json()
        return response
