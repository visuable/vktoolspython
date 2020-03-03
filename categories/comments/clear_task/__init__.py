import time

from categories.basic_task import Task
from extra import cascade_owner_id_post_id
from extra import select_ids_from_labeled_news_feed


class ClearCommentsTask(Task):
    __user_identifier = ''

    def __init__(self, params, user_identifier):
        self.__user_identifier = user_identifier
        super(ClearCommentsTask, self).__init__(params=params)

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
                while True:
                    # Получаем список комментариев
                    temp_response = self.user_api_request('https://api.vk.com/method/wall.getComments',
                                                          params=request).json()
                    # Нужно, если будет возвращена ошибка
                    try:
                        # Начало запроса - конец предыдущего, т.е смещение
                        request['start_comment_id'] = temp_response['response']['items'][-1]['id']
                    except Exception:
                        break
                    if 'real_offset' not in temp_response['response']:
                        continue
                    # Ключ может не всегда быть в словаре, и если его нет будет выдано исключение
                    real_offset_count = int(temp_response['response']['real_offset'])
                    # -1 не работает: real_offset всегда на 1 меньше, а current_level_count на 1 больше
                    full_count = (int(temp_response['response']['current_level_count']) - 2)
                    # Чтобы всегда было смещение, нужно сделать так,
                    # Чтобы количество полученных комментариев было меньше,
                    # Чем их общее кол-во
                    if real_offset_count <= full_count:
                        for item in temp_response['response']['items']:
                            # Тут может быть возвращена ошибка, поэтому блок обернут в try
                            try:
                                # Проверка, если отправил данный пользователей, то удаляем комментарий
                                if int(self.__user_identifier) == int(item['from_id']):
                                    payload = {
                                        'owner_id': item['owner_id'],
                                        'comment_id': item['id']}
                                    self.user_api_request(
                                        'https://api.vk.com/method/wall.deleteComment',
                                        params=payload)
                                    break
                            except Exception:
                                continue
                    else:
                        break
                    # По документации: частота обращения не чаще, чем в раз в 3 секунды
                    time.sleep(3)

    def __get_posts_from_news_feed_section_comments(self):
        try:
            feed_response = self.site_request('https://vk.com/feed?section=comments').text
            ids = select_ids_from_labeled_news_feed(feed_response)
            return ids
        except Exception:
            pass
