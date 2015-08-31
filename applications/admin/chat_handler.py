# coding=utf-8
__author__ = 'wan'
from tornado.web import authenticated
from common.base import BaseHandler
from services.admin.user_service import UserService
from tornado.websocket import WebSocketHandler
from common.redis_cache import RedisCacheManager
from tornado import gen
import json

class ChatHandler(BaseHandler):
    """ 聊天室 """
    @authenticated
    def get(self):
        user_ser = UserService(self.db)
        user_id = self.get_current_user()

        cur_user = user_ser.get_user_by_uuid(user_id)
        users = user_ser.get_all_user_order_by_active()
        return self.render('chat.html', users=users, cur_user=cur_user)


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
    def get(self):
        redis_ser = RedisCacheManager()
        all_users = self.get_user_info_from_mysql()
        total_count = redis_ser.get('total_count')
        active_count = redis_ser.get('active_count')

        if not total_count:
            redis_ser.set('total_count', self.get_user_count())
            total_count = redis_ser.get('total_count')

        if not active_count:
            redis_ser.set('active_count', self.get_active_count())
            active_count = redis_ser.get('active_count')

        return self.render('ajax/user_info.html', users=all_users, total_count=total_count, active_count=active_count)


    def get_user_info_from_mysql(self):
        user_ser = UserService(self.db)
        all_user = user_ser.get_all_user_order_by_active()
        return all_user
        # user_list = []
        # for u in all_user:
        #     user_info = {}
        #     user_info[u.user_name] = u.user_name
        #     user_info[u.user_id] = u.user_id
        #     user_info[u.avatar] = u.avatar
        #     user_list.append(user_info)

        # return json.dumps(user_list)

    def get_user_count(self):
        user_ser = UserService(self.db)
        return user_ser.get_user_count()

    def get_active_count(self):
        user_ser = UserService(self.db)
        return user_ser.get_user_count_by_active()

