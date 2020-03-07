from categories.auth.auth_settings import AuthSettings
from categories.auth.auth_task import AuthTask

if __name__ == '__main__':
    login = '89181872554'
    password = 'hjr23m40q'
    auth_task = AuthTask(AuthSettings(login, password))
    auth_task.run()
