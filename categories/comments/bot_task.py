from loguru import logger
from lxml import etree

from categories.basic_task import Task
from extra import cascade_owner_id_post_id, dict_merge
from extra import select_ids_from_news_feed, delta_time_from_now


class CommentBotTask(Task):
    __message = ''
    __count = 0

    # Перегрузка базового конструктора
    def __init__(self, params, message, count):
        super(CommentBotTask, self).__init__(params)
        self.__message = message
        self.__count = count

    def run(self):
        completed = {}
        while len(completed) <= self.__count:
            post_parameters_cascade, times = self.__get_post_date_from_news_feed()
            for post, time_ in zip(post_parameters_cascade, times):
                # Если пост старый, то пропускаем, время в юникс-штампе (секундах)
                if delta_time_from_now(time_) > 10:
                    logger.trace('Пост пропущен по времени')
                    continue
                # Если под постом уже оставлен комментарий, то тоже пропускаем
                if str(post) in completed:
                    logger.trace('Пост пропущен по словарю')
                    continue
                # Запрос на добавление комментария
                create_comment_query = dict_merge({'message': self.__message},
                                                  {'owner_id': post[0], 'post_id': post[1]})
                response = self.user_api_request('https://api.vk.com/method/wall.createComment',
                                                 **create_comment_query).json()
                # Если запрос прошел, то добавляем идентификатор поста в список завершенных задач
                if 'response' in response:
                    completed[str(post)] = response['response']
                    logger.success('Комментарий оставлен и добавлен в словарь')

    def __get_post_date_from_news_feed(self):
        # Получаем страницу новостей
        try:
            feed_html_response_text = self.site_request('https://vk.com/feed').text
            # Извлекаем отсюда все идентификаторы постов
            post_parameters_cascade = cascade_owner_id_post_id(select_ids_from_news_feed(feed_html_response_text))
            # Из них достаем даты с помощью XPath
            times = etree.HTML(feed_html_response_text).xpath('//span[@class=\'rel_date rel_date_needs_update\']/@time')
            logger.trace('Даты постов получены')
            return post_parameters_cascade, times
        except Exception:
            pass
