#Site URLs

OAUTH_AUTH = 'https://oauth.vk.com/authorize'
REDIRECT_URI = 'https://oauth.vk.com/blank.html'
VK_MOBILE = 'https://m.vk.com'
VK_FEED = 'https://vk.com/feed'
VK_COMMENTS_FEED = 'https://vk.com/feed?section=comments'
VK_LIKES_FEED = 'https://vk.com/feed?section=likes'

#API URLs

CREATE_COMMENT = 'https://api.vk.com/method/wall.createComment'
GET_COMMENTS = 'https://api.vk.com/method/wall.getComments'
USERS_GET = 'https://api.vk.com/method/users.get'
DELETE_COMMENTS = 'https://api.vk.com/method/wall.deleteComment'
LIKES_DELETE = 'https://api.vk.com/method/likes.delete'
WALL_DELETE = 'https://api.vk.com/method/wall.delete'
WALL_GET = 'https://api.vk.com/method/wall.get'

#Типы

TYPES = ['comment',
             'photo',
             'video',
             'post',
             'audio',
             'note',
             'photo_comment',
             'video_comment',
             'topic_comment',
             'sitepage']