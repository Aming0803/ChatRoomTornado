# coding=utf-8
__author__ = 'wan'
from common.function_wraper import singleton
from common.redis_cache import RedisCacheManager
from services.admin.user_service import UserService
from common.base import DB

@singleton
class ChatManager(object):
    def __init__(self):
        """获取在线人数"""
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


@singleton
class MultPersonChatManger(object):
    def __init__(self):
        """
        多人聊天，waits存储等待的人，cache存储消息，size最大消息数
        :return:
        """
        self.waits = set()
        self.cache = []
        self.cache_size = 100

    def new_message(self, record):
        for future in self.waits:
            future.set_result(record)
        self.waits = set()
        self.cache.append(record)
        if len(self.cache)>self.cache_size:
            self.cache = self.cache[-self.cache_size:]

    def update_message(self, future):
        self.waits.add(future)

    def cancle_wait(self, future):
        self.waits.remove(future)


@singleton
class MessageRealTimePush(object):
    def __init__(self):
        """
        消息实时推送
        :return:
        """
        self.waits = {}

    def update_waits(self, future, user_id):

        if user_id not in self.waits:
            self.waits[user_id] = [future]
        else:
            self.waits[user_id].append(future)

    def send_message(self, chat, user_id):
        #每次队列中只有一个future,set_result后即删除
        try:
            future = self.waits[user_id].pop()
            future.set_result(chat)
        except Exception,e:
            print e

