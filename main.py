from categories.auth.auth_task import AuthTask
from categories.comments.bot_task import CommentBotTask
from categories.comments.clear_task import ClearCommentsTask
from categories.newsfeed.clear_task import ClearLikesTask
from categories.wall.clear_task import WallCleanerTask

if __name__ == '__main__':
    login = input('Введите свой логин: ').strip()
    password = input('Введите свой пароль: ').strip()
    params = AuthTask(login, password).run()
    task_number = input('Введите номер задачи: \n'
                        '1 -- Бот комментатор \n'
                        '2 -- Очистка аккаунта от комментариев \n'
                        '3 -- Очистка понравившихся записей на аккаунте \n'
                        '4 -- Очистка стены \n')
    if task_number == '1':
        message = input('Введите текст комментария: \n')
        count = input('Введите количество комментариев: \n')
        bot = CommentBotTask(params, message, int(count)).run()
        pass
    if task_number == '2':
        clear = ClearCommentsTask(params).run()
        pass
    if task_number == '3':
        clear = ClearLikesTask(params).run()
        pass
    if task_number == '4':
        clear = WallCleanerTask(params).run()
        pass
