#coding=utf-8
import platform


#mysql
if platform.system() == 'Linux':
    #under ubuntu
    DB_CONNECT_STRING = 'mysql://root:root@localhost/chatroom?charset=utf8'
if platform.system() == 'Darwin':
    #under mac
    DB_CONNECT_STRING = 'mysql://root:ysletmein@localhost/chatroom?charset=utf8'

#redis
REDIS_PORT = 6379
REDIS_HOST = '127.0.0.1'

#Celery
REDIS_CELERY_BROKER = 'redis://127.0.0.1:6379/1'

#人数是否发生了变化

IS_COUNT_CHANGE = False
# conn = pymongo.Connection("localhost", 27017)
# self.db = conn['mytest']					