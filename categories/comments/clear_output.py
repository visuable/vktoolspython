from categories.utils.output import Output


class ClearOutput(Output):
    def show(self, response):
        if response['response']:
            print('Комментарий удален')
        else:
            print('Ошибка')