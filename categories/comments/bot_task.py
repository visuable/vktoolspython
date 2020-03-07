from lxml import etree

from categories.basic_task import Task
from categories.comments.bot_settings import BotSettings
from constants import CREATE_COMMENT, VK_FEED
from extra import cascade_owner_id_post_id, dict_merge
from extra import select_ids_from_news_feed, delta_time_from_now


class CommentBotTask(Task):
    bot_settings = BotSettings(None, '', 0, 0)

    # Перегрузка базового конструктора
    def __init__(self, bot_settings):
        self.bot_settings = bot_settings
        super(CommentBotTask, self).__init__(bot_settings)

    def run(self):
        completed = {}
        while len(completed) <= self.bot_settings.count:
            post_parameters_cascade, times = self.__get_post_date_from_news_feed()
            for post, time_ in zip(post_parameters_cascade, times):
                # Если пост старый, то пропускаем, время в юникс-штампе (секундах)
                if delta_time_from_now(time_) > self.bot_settings.time:
                    continue
                # Если под постом уже оставлен комментарий, то тоже пропускаем
                if str(post) in completed:
                    continue
                # Запрос на добавление комментария
                create_comment_query = dict_merge({'message': self.bot_settings.message},
                                                  {'owner_id': post[0], 'post_id': post[1]})
                response = self.user_api_request(CREATE_COMMENT,
                                                 **create_comment_query).json()
                # Если запрос прошел, то добавляем идентификатор поста в список завершенных задач
                if 'response' in response:
                    completed[str(post)] = response['response']

    def __get_post_date_from_news_feed(self):
        # Получаем страницу новостей
        feed_html_response_text = self.site_request(VK_FEED).text
        # Извлекаем отсюда все идентификаторы постов
        post_parameters_cascade = cascade_owner_id_post_id(select_ids_from_news_feed(feed_html_response_text))
        # Из них достаем даты с помощью XPath
        times = etree.HTML(feed_html_response_text).xpath('//span[@class=\'rel_date rel_date_needs_update\']/@time')
        return post_parameters_cascade, times
