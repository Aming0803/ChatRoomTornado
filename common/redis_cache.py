#coding=utf-8
__author__ = 'wan'

from common.config import REDIS_HOST, REDIS_PORT
from common.function_wraper import singleton
import redis


@singleton
class RedisCacheManager(object):
    def __init__(self):
        pass

    @property
    def _con(self):
        pool = redis.ConnectionPool(REDIS_HOST, REDIS_PORT)
        return redis.Redis(connection_pool=pool)

    def set(self, key, value):
        """
        字符串的存取
        :param key:
        :param value:
        :return:
        """
        return self._con.set(key, value)

    def get(self, key):
        return self._con.get(key)

    def incr(self, key, amount=1):
        return self._con.incr(key, amount)

    def h_set(self, name, key, data):
        """
        哈希值的存取
        :param key:
        :param data:
        :return:
        """
        return self._con.hset(name, key, data)

    def h_get(self, name, key):
        return self._con.hget(name, key)

    def h_get_all(self, name):
        return self._con.hgetall(name)

    def hm_set(self, key, value):
        """
        存储字典
        :param key:
        :param value:
        :return:
        """
        return self._con.hmset(key, value)

    def hm_get(self, key):
        return self._con.hgetall(key)