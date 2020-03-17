from categories.auth.auth_settings import AuthSettings
from categories.auth.auth_task import AuthTask
from categories.comments.bot_settings import BotSettings
from categories.comments.bot_task import CommentBotTask
from categories.comments.clear_task import ClearCommentsTask
from categories.comments.spammer_settings import SpammerSettings
from categories.comments.spammer_task import SpammerTask
from categories.settings import Settings

if __name__ == '__main__':
    login = '89254917386'
    password = 'ssss271104as'
    auth_task = AuthTask(AuthSettings(login=login, password=password))
    result = auth_task.run()
    # clear_task = ClearCommentsTask(Settings(params=result))
    # clear_task.run()
    # bot_task = CommentBotTask(BotSettings(params=result, message='lol', count=5, time=1000000))
    # bot_task.run()
    spam_task = SpammerTask(SpammerSettings(params=result, interval=3, primary_count=2, user_id=546688952, message='111test', secondary_count=10))
    spam_task.run()
