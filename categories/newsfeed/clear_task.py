import time

from categories.basic_task import Task
from categories.utils.constants import TYPES, LIKES_DELETE, VK_LIKES_FEED
from categories.utils.extra import select_ids_from_labeled_news_feed


class ClearLikesTask(Task):

    def __init__(self, settings):
        super(ClearLikesTask, self).__init__(settings)

    def run(self):
        while True:
            identifiers = self.__get_posts_from_news_feed_section_likes()
            if not len(identifiers):
                break
            # Каждый запрос на 4 типа: если запрос проходит, то цикл останавливается
            for identifier in identifiers:
                for request_type in TYPES:
                    # Задержка из-за ограничения по документации метода
                    time.sleep(3)
                    # Запрос на удаление лайка
                    likes_delete_response = self.__likes_delete_request({'owner_id': identifier[0],
                                                                         'item_id': identifier[1],
                                                                         'type': request_type})
                    try:
                        if int(likes_delete_response['response']['likes']):
                            break
                    except Exception:
                        continue

    def __likes_delete_request(self, request):
        try:
            likes_delete_response = self.user_api_request(LIKES_DELETE, **request).json()
            return likes_delete_response
        except Exception:
            pass

    def __get_posts_from_news_feed_section_likes(self):
        try:
            feed_response = self.site_request(VK_LIKES_FEED).text
            ids = select_ids_from_labeled_news_feed(feed_response)
            return ids
        except Exception:
            pass
