from categories.auth.auth_settings import AuthSettings
from categories.auth.auth_task import AuthTask
from categories.comments.bot_settings import BotSettings
from categories.comments.bot_task import CommentBotTask
from categories.comments.clear_task import ClearCommentsTask
from categories.settings import Settings

if __name__ == '__main__':
    login = '89254917386'
    password = 'ssss271104as'
    auth_task = AuthTask(AuthSettings(login=login, password=password))
    result = auth_task.run()
    clear_task = ClearCommentsTask(Settings(params=result))
    clear_task.run()