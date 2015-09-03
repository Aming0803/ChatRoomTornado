# coding=utf-8
__author__ = 'wan'
from common.function_wraper import singleton
from common.redis_cache import RedisCacheManager
from services.admin.user_service import UserService
from common.base import DB

@singleton
class ChatManager(object):
    def __init__(self):
        self.count_waits = set()

    def get_info(self, future):

        redis_ser = RedisCacheManager()

        total_count = redis_ser.get('total_count')
        active_count = redis_ser.get('active_count')

        data = {
            'total_count':total_count,
            'active_count':active_count,
            'all_users':self.get_all_user()
        }
        future.set_result(data)

    def get_all_user(self):
        user_ser = UserService(DB)
        all_user = user_ser.get_all_user_order_by_active()
        return all_user