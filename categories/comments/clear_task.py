import time

from categories.basic_task import Task
from constants import WALL_GET_COMMENTS, USERS_GET, WALL_DELETE_COMMENTS, VK_COMMENTS_FEED
from extra import cascade_owner_id_post_id
from extra import select_ids_from_labeled_news_feed


class ClearCommentsTask(Task):

    def __init__(self, settings):
        super(ClearCommentsTask, self).__init__(settings)

    def run(self):
        while True:
            # Получение страницы новостей с комментариями
            ids = self.__get_posts_from_news_feed_section_comments()
            # Если понравившиеся кончились, то останавливаем цикл
            if not len(ids):
                break
            requests = []
            for identifier in ids:
                # Запрос на метод wall.getComments
                (owner_id, post_id) = cascade_owner_id_post_id(identifier)
                requests.append({'owner_id': owner_id,
                                 'post_id': post_id,
                                 'sort': 'asc',
                                 'need_likes': '0',
                                 'count': '100'})
            for request in requests:
                responses = []
                while True:
                    # Получаем список комментариев
                    temp_response = self.user_api_request(WALL_GET_COMMENTS,
                                                          **request).json()
                    responses.append(temp_response)
                    # Задаем смещение
                    last_post_id = temp_response['response']['items'][-1]['id']
                    request['start_comment_id'] = last_post_id
                    if len(temp_response['response']['items']) < 100:
                        break
                    # По документации: частота обращения не чаще, чем в раз в 3 секунды
                    time.sleep(3)
                for response in responses:
                    for item in response['response']['items']:
                        if self.user_id == item['from_id']:
                            self.user_api_request(WALL_DELETE)


    def __get_posts_from_news_feed_section_comments(self):
        try:
            feed_response = self.site_request(VK_COMMENTS_FEED).text
            ids = select_ids_from_labeled_news_feed(feed_response)
            return ids
        except Exception:
            pass
