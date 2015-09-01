# coding=utf-8
__author__ = 'wan'

from common.redis_cache import RedisCacheManager

def main():
    redis_ser = RedisCacheManager()
    redis_ser._con.flushdb()

if __name__ == '__main__':
    main()