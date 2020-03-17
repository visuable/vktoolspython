import re
import time

from lxml import etree


def select_ids_from_news_feed(feed_response):
    document = etree.HTML(feed_response)
    feed_rows = document.xpath('.//div[@class="feed_row "]/div/@data-post-id')
    ids = extract_rows(feed_rows)
    return ids


def select_ids_from_labeled_news_feed(feed_response):
    document = etree.HTML(feed_response)
    feed_rows = document.xpath('.//div[@class="feed_row"]/div/@data-post-id')
    ids = extract_rows(feed_rows)
    return ids


def extract_rows(feed_rows):
    ids = []
    for feed_row in feed_rows:
        ids.append(re.findall(pattern='\d+', string=feed_row))
    return ids


def join_posts(ids):
    return ','.join(ids)


def dict_merge(a, b):
    return a.update(b) or a


def parse_token(oauth_token_response_url):
    try:
        token_string = re.findall('access_token=([^&]*)', oauth_token_response_url)[0]
        return token_string
    except Exception:
        pass


def delta_time_from_now(time2):
    return int(time.time()) - int(time2)


def wait_for_request(request):
    while True:
        try:
            time.sleep(3)
            return request()
        except Exception:
            pass
