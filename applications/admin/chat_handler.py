# coding=utf-8
__author__ = 'wan'
from tornado.web import authenticated
from common.base import BaseHandler
from services.admin.user_service import UserService
from tornado.websocket import WebSocketHandler


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
        pass