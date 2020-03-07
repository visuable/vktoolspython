import time

from loguru import logger

from categories.basic_task import Task
from extra import cascade_owner_id_post_id
from extra import select_ids_from_labeled_news_feed


class ClearLikesTask(Task):
    types = ['comment',
             'photo',
             'video',
             'post',
             'audio',
             'note',
             'photo_comment',
             'video_comment',
             'topic_comment',
             'sitepage']

    def __init__(self, settings):
        super(ClearLikesTask, self).__init__(settings)

    def run(self):
        while True:
            ids = self.__get_posts_from_news_feed_section_likes()
            if not len(ids):
                break
            # Каждый запрос на 4 типа: если запрос проходит, то цикл останавливается
            for identifier in ids:
                (owner_id, post_id) = cascade_owner_id_post_id(identifier)
                for type_ in self.types:
                    # Задержка из-за ограничения по документации метода
                    time.sleep(5)
                    # Запрос на удаление лайка
                    likes_delete_response = self.__likes_delete_request({'owner_id': owner_id,
                                                                         'item_id': post_id,
                                                                         'type': type_})
                    try:
                        if int(likes_delete_response['response']['likes']):
                            logger.success('Лайк убран')
                            break
                    except Exception:
                        logger.error('Выдана ошибка из ответа сервера')
                        continue

    def __likes_delete_request(self, request):
        try:
            likes_delete_response = self.user_api_request('https://api.vk.com/method/likes.delete', **request).json()
            logger.trace('Запрос на удаление')
            return likes_delete_response
        except Exception:
            pass

    def __get_posts_from_news_feed_section_likes(self):
        try:
            feed_response = self.site_request('https://vk.com/feed?section=likes').text
            ids = select_ids_from_labeled_news_feed(feed_response)
            logger.trace('Посты получены')
            return ids
        except Exception:
            pass
