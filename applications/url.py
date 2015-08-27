#coding=utf-8
__author__ = 'wan'

from admin.user_handler import LoginHandler, RegisterHandler


handlers = [
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),

]