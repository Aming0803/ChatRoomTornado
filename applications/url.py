#coding=utf-8
__author__ = 'wan'

from admin.user_handler import LoginHandler, RegisterHandler, IndexHandler, LogoutHandler
from admin.chat_handler import ChatHandler, OneToOneChaHandler, ChatGetUserCount, \
    ChatNewMessageHandler, ChatUpdateMessageHandler, ChatOneToOneBySocketHandler, MessageRTPushHandler

handlers = [
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),
    (r'/logout', LogoutHandler),

    (r'/chat', ChatHandler),
    (r'/single_chat', OneToOneChaHandler),

    (r'/get_count', ChatGetUserCount),
    (r'/message/new', ChatNewMessageHandler),
    (r'/message/update', ChatUpdateMessageHandler),
    (r'/websocket/single', ChatOneToOneBySocketHandler),

    (r'/message/push', MessageRTPushHandler),

]