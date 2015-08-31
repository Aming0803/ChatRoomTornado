#coding=utf-8
__author__ = 'wan'

from dao.admin.user_dao import UserDao
from models.user_do import UserDO
import time
import logging
log = logging.getLogger(__file__)


class UserService(object):
    """ 用户的service层 """
    def __init__(self, db):
        self.db = db
        self.dao = UserDao(self.db)
    def get_user_by_id(self, id):
        user_dao = UserDao(self.db)
        return user_dao.get_user_by_id(id)

    def get_user_by_uuid(self, user_id):
        user_dao = UserDao(self.db)
        return user_dao.get_user_by_uuid(user_id)

    def create_user(self, params):
        user_dao = UserDao(self.db)
        log.info('create user by params:%s'%params)
        try:
            user_do = UserDO()
            user_do.is_active = False
            user_do.is_admin = False
            user_do.user_id = self.create_uuid()
            for param in params:
                setattr(user_do, param, params[param])
            return user_dao.create_user(user_do)
        except Exception, e:
            log.error(e)
            return False, e

    def create_uuid(self):
        return '%.0f'% (time.time()*1000000)

    def get_user_by_name_and_pwd(self, name, pwd):
        user_dao = UserDao(self.db)
        return user_dao.get_user_by_name_and_pwd(name, pwd)

    def get_all_user_order_by_active(self):
        user_dao = UserDao(self.db)
        return user_dao.get_all_user_by_order()

    def get_user_count(self):
        return self.dao.get_user_count()

    def get_user_count_by_active(self):
        return self.dao.get_user_count_by_active()