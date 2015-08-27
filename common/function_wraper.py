#coding=utf-8
__author__ = 'wan'


def singleton(cls, *args, **kwargs):
    """
    单实例模式
    :param cls:
    :param args:
    :param kwargs:
    :return:
    """
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton