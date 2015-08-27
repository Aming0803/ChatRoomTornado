#coding=utf-8
__author__ = 'wan'

from admin.user_handler import LoginHandler, RegisterHandler
from admin.chat_handler import ChatHandler

handlers = [
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),

    (r'/chat', ChatHandler),

]