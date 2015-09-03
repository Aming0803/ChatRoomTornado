# coding=utf-8
__author__ = 'wan'
from tornado.web import authenticated
from common.base import BaseHandler
from services.admin.user_service import UserService
from tornado.websocket import WebSocketHandler
from common.redis_cache import RedisCacheManager
from tornado.gen import coroutine
from tornado.concurrent import Future
from tornado.web import asynchronous
from common.chat_tool import ChatManager


class ChatHandler(BaseHandler):
    """ 聊天室 """
    @authenticated
    def get(self):
        user_ser = UserService(self.db)
        user_id = self.get_current_user()

        cur_user = user_ser.get_user_by_uuid(user_id)
        users = user_ser.get_all_user_order_by_active()

        redis_ser = RedisCacheManager()
        redis_ser._con.flushdb()

        active_count = redis_ser.get('active_count')
        total_count = redis_ser.get('total_count')

        if not active_count or not total_count:
            pipe = redis_ser._con.pipeline()
            pipe.set('total_count', self.get_user_count())
            pipe.set('active_count', self.get_active_count())
            pipe.execute()
            active_count = redis_ser.get('active_count')
            total_count = redis_ser.get('total_count')

        data = {
            'total_count':total_count,
            'active_count':active_count,
            'users':users
        }

        return self.render('chat.html', data=data, cur_user=cur_user)

    def get_user_count(self):
        user_ser = UserService(self.db)
        return user_ser.get_user_count()

    def get_active_count(self):
        user_ser = UserService(self.db)
        return user_ser.get_user_count_by_active()

class OneToOneChaHandler(BaseHandler):
    """ 一对一聊天 """

    def get(self):
        user_ser = UserService(self.db)
        user_id = self.get_current_user()

        cur_user = user_ser.get_user_by_uuid(user_id)
        return self.render('single_chat.html', cur_user=cur_user)


class ChatGetUserCount(BaseHandler):
    """ 聊天室获取总人数和在线的人数 """
    @authenticated
    @coroutine
    def get(self):
        self.future = Future()
        ChatManager().count_waits.add(self.future)
        data = yield self.future
        if self.request.connection.stream.closed():
            return
        self.render('ajax/user_info.html', data=data)

    def on_connection_close(self):
        ChatManager().count_waits.remove(self.future)
        self.future.set_result([])


class ChatMorePHandler(BaseHandler):
    """多人聊天"""
    def get(self):
        return self




