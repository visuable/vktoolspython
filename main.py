from categories.advanced_task import AdvTask
from categories.auth.adv_auth_task import AdvAuthTask
from categories.auth.auth_settings import AuthSettings
from categories.auth.auth_task import AuthTask
from categories.comments.clear_task import ClearCommentsTask
from categories.comments.spammer_task import SpammerTask
from categories.music.converter_task import ConverterTask
from categories.newsfeed.clear_task import ClearLikesTask
from categories.settings.settings import Settings
from categories.settings.spammer_settings import SpammerSettings

if __name__ == '__main__':
    login = '89254917386'
    password = 'ssss271104as'
    # auth_task = AuthTask(AuthSettings(login=login, password=password))
    # result = auth_task.run()
    # # clear_task = ClearCommentsTask(Settings(params=result))
    # # clear_task.run()
    # # news_clear_task = ClearLikesTask(Settings(params=result))
    # # news_clear_task.run()
    # converter = ConverterTask(Settings(params=result))
    # converter.run()
    # bot_task = CommentBotTask(BotSettings(params=result, message='lol', count=5, time=1000000))
    # bot_task.run()
    # spam_task = SpammerTask(
    #     SpammerSettings(params=result, interval=3, primary_count=2, user_id=546688952, message='111test',
    #                     secondary_count=10))
    # spam_task.run()
    auth = AdvAuthTask(AuthSettings(login=login, password=password))
    ressult = auth.run()
    print(ressult)

