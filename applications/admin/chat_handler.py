# coding=utf-8
__author__ = 'wan'
from tornado.web import authenticated
from common.base import BaseHandler
from services.admin.user_service import UserService
from tornado.websocket import WebSocketHandler
from common.redis_cache import RedisCacheManager
from tornado.gen import coroutine
from tornado.concurrent import Future
# from tornado.web import asynchronous
# from tornado.httpclient import AsyncHTTPClient
from common.chat_tool import ChatManager, MultPersonChatManger, MessageRealTimePush
from tornado.escape import to_basestring
from common.base import DB
import datetime
import json


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

        records = MultPersonChatManger().cache

        return self.render('chat.html', data=data, cur_user=cur_user, records=records)

    def get_user_count(self):
        user_ser = UserService(self.db)
        return user_ser.get_user_count()

    def get_active_count(self):
        user_ser = UserService(self.db)
        return user_ser.get_user_count_by_active()


class OneToOneChaHandler(BaseHandler):
    """ 一对一聊天跳转页面 """
    @authenticated
    def get(self):
        redis_ser = RedisCacheManager()
        user_ser = UserService(self.db)
        user_id = self.get_current_user()
        to_user_id = self.get_argument('to_user_id')

        cur_user = user_ser.get_user_by_uuid(user_id)
        to_user = user_ser.get_user_by_uuid(to_user_id)

        records = redis_ser.hm_get(user_id)


        return self.render('single_chat.html', cur_user=cur_user, to_user=to_user, records=[records])


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


class ChatNewMessageHandler(BaseHandler):
    """多人聊天"""
    def post(self):
        user_ser = UserService(self.db)

        message = self.get_argument('message', None)
        if not message:
            return self.write('error')

        user_id = self.get_current_user()
        user_name = user_ser.get_name_by_user_id(user_id)
        avatar = user_ser.get_avatar_by_user_id(user_id)

        record = {
            'message':message,
            'user_id':user_id,
            'name':user_name,
            'avatar':avatar,
            'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.write('success')
        self.save_by_redis(record)

        MultPersonChatManger().new_message(record)

    def save_by_redis(self, record):
        redis_ser = RedisCacheManager()
        key = datetime.datetime.now().strftime('%Y-%m-%d')
        record_str = json.dumps(record)
        redis_ser.save_in_list(key, record_str)


class ChatUpdateMessageHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        self.future = Future()
        MultPersonChatManger().update_message(self.future)
        data = yield self.future

        if self.request.connection.stream.closed():
            return
        self.render('ajax/message.html', data=data)

    def on_connection_close(self):
        MultPersonChatManger().waits.remove(self.future)
        self.future.set_result([])
        self.decr_active_count()
        self.update_user_active(self.get_current_user())

    def decr_active_count(self):
        redis_ser = RedisCacheManager()
        redis_ser.decr('active_count')

    def update_user_active(self, user_id):
        user_ser = UserService(self.db)
        user = user_ser.get_user_by_uuid(user_id)
        user.is_active = 0
        self.db.commit()

class ChatOneToOneBySocketHandler(WebSocketHandler):
    """利用websocket实现一对一聊天"""
    watis = {}
    cache_size = 100

    def get_compression_options(self):
        return {}

    def open(self):
        """
        waits为字典是为了存储多个一对一聊天，根据聊天双方user_id拼凑聊天室id
        字典中在包含字典，一个存储用户对象，一个存储聊天记录
        :return:
        """
        to_user = self.get_argument('to_user_id', None)

        if not to_user:
            return self.write('error!!!')
        cur_user = self.get_current_user()
        key = self.get_wait_key(cur_user, to_user)

        if key not in ChatOneToOneBySocketHandler.watis:
            ChatOneToOneBySocketHandler.watis[key] = {}
            ChatOneToOneBySocketHandler.watis[key]['waits'] = [self]
            ChatOneToOneBySocketHandler.watis[key]['cache'] = []

        else:
            ChatOneToOneBySocketHandler.watis.get(key).get('waits').append(self)

    def on_close(self):
        to_user = self.get_argument('to_user_id', None)

        if not to_user:
            return self.write('error!!!')

        cur_user = self.get_current_user()
        key = self.get_wait_key(cur_user, to_user)
        ChatOneToOneBySocketHandler.watis.get(key).get('waits').remove(self)
        self.decr_active_count()
        self.update_user_active(self.get_current_user())


    def on_message(self, message):
        to_user = self.get_argument('to_user_id', None)

        user_ser = UserService(self.application.db)
        message = json.loads(message)
        from_user = self.get_current_user()

        key = self.get_wait_key(from_user, to_user)
        user =user_ser.get_user_by_uuid(from_user)
        chat = {
            'message':message.get('info'),
            'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_id':from_user,
            'avatar':user.avatar,
            'name':user.user_name
        }
        now_waits = ChatOneToOneBySocketHandler.watis.get(key).get('waits')
        now_cache = ChatOneToOneBySocketHandler.watis.get(key).get('cache')

        #说明另一个人此时不在对话中，所以发送消息给他
        if len(now_waits) < 2:
            redis_ser = RedisCacheManager()
            MessageRealTimePush().send_message(chat, to_user)
            redis_ser.hm_set(to_user, chat)

        self.update_cache(now_cache, chat)
        self.send_to_update(now_waits, chat)

    def get_wait_key(self, cur_user, to_user):
        user_list = []
        user_list.append(to_user)
        user_list.append(cur_user)
        new_user_list = sorted(user_list)
        key = '-'.join(new_user_list)
        return key

    def update_cache(self, cache, chat):

        cache.append(chat)
        if len(cache)>ChatOneToOneBySocketHandler.cache_size:
            cache = cache[-ChatOneToOneBySocketHandler.cache_size:]
        return cache

    def send_to_update(self, waits, chat):
        current_user = self.get_current_user()
        html_info = {}
        html_info['user'] = current_user
        html_info['html'] = to_basestring(self.render_string("ajax/single_message.html", data=chat))
        for wait in waits:
            wait.write_message(html_info)

    def get_current_user(self):
        return self.get_secure_cookie('user_id')

    def decr_active_count(self):
        redis_ser = RedisCacheManager()
        redis_ser.decr('active_count')

    def update_user_active(self, user_id):
        user_ser = UserService(DB)
        user = user_ser.get_user_by_uuid(user_id)
        user.is_active = 0
        DB.commit()


class MessageRTPushHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        user_id = self.get_current_user()
        self.future = Future()
        MessageRealTimePush().update_waits(self.future, user_id)
        data = yield self.future

        if self.request.connection.stream.closed():
            return
        # result = to_basestring(self.render('ajax/push.html', data=data))
        self.render('ajax/push.html', data=data)

    def on_connection_close(self):
        user_id = self.get_current_user()
        MessageRealTimePush().update_waits(self.future, user_id)
        self.future.set_result([])



