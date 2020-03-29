def parse_error(response):
    if 'error' in response:
        error = response['error']
        erc = error['error_code']
        if erc == 15:
            print('Ошибка доступа: ', error['error_msg'])
        elif erc == 14:
            print('Капча: ', 'Идентификатор: ', error['captcha_sid'], 'URL: ', error['captcha_img'])
        return True
    return False
# {'error': {'error_code': 15, 'error_msg': 'Access denied: post was not found check post_id param',
#                               'request_params': [{'key': 'v', 'value': '5.103'},
#                                                  {'key': 'owner_id', 'value': '156971067'},
#                                                  {'key': 'post_id', 'value': '386436'}, {'key': 'sort', 'value': 'asc'},
#                                                  {'key': 'need_likes', 'value': '0'}, {'key': 'count', 'value': '100'},
#                                                  {'key': 'thread_items_count', 'value': '10'},
#                                                  {'key': 'method', 'value': 'wall.getComments'},
#                                                  {'key': 'oauth', 'value': '1'}]}}