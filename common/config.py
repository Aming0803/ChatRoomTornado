#coding=utf-8

#mysql
DB_CONNECT_STRING = 'mysql://root:root@localhost/chatroom?charset=utf8'

#redis
REDIS_PORT = 6379
REDIS_HOST = '127.0.0.1'

#Celery
REDIS_CELERY_BROKER = 'redis://127.0.0.1:6379/1'


# conn = pymongo.Connection("localhost", 27017)
# self.db = conn['mytest']					