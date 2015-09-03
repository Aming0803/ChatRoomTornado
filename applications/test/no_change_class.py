# coding=utf-8
__author__ = 'wan'
# from common
from common.function_wraper import singleton


@singleton
class NoChangeClass(object):
    def __init__(self):
        self.waits = set()
        self.cache = []



def main():
    a = NoChangeClass()
    b = NoChangeClass()
    a.waits.add('a')
    a.cache.append('a')
    print b.waits
    print b.cache

if __name__ == '__main__':
    main()