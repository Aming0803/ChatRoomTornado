#coding=utf-8
__author__ = 'wan'

from admin.user_handler import LoginHandler, RegisterHandler, IndexHandler
from admin.chat_handler import ChatHandler, OneToOneChaHandler, ChatGetUserCount

handlers = [
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),

    (r'/chat', ChatHandler),
    (r'/single_chat', OneToOneChaHandler),

    (r'/get_count', ChatGetUserCount),

]