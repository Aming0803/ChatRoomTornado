# coding=utf-8
__author__ = 'wan'
from tornado.web import authenticated
from common.base import BaseHandler


class ChatHandler(BaseHandler):
    """ 聊天室 """
    @authenticated
    def get(self):
        return self.render('chatlist.html')