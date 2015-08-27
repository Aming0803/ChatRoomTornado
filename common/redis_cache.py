#coding=utf-8
__author__ = 'wan'

from common.config import REDIS_HOST, REDIS_PORT
from common.function_wraper import singleton
import redis

class RedisCacheManager(object):
    def __init__(self):
        pass

    @property
    def _con(self):
        pool = redis.ConnectionPool(REDIS_HOST, REDIS_PORT)
        return redis.Redis(connection_pool=pool)