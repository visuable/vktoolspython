from categories.utils.output import Output


class SpammerOutput(Output):
    def show(self, response):
        print('Комментарий оставлен: ', response['response']['comment_id'])