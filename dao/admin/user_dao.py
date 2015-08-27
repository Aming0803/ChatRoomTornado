#coding=utf-8
__author__ = 'wan'
from models.user_do import UserDO
from sqlalchemy import and_

import logging
log = logging.getLogger(__file__)


class UserDao(object):

    def __init__(self, db):
        self.db = db

    @property
    def get_query(self):
        return self.db.query(UserDO)

    def create_user(self, user_do):
        try:
            self.get_query.add(user_do)
            self.db.commit()
            return True, ''
        except Exception, e:
            log.error(e)
            return False, e

    def get_user_by_id(self, id):
        return self.get_query.filter_by(and_(id=id, deleted=False)).first()

    def get_user_by_uuid(self, user_id):
        return self.get_query.filter_by(and_(id=user_id, deleted=False)).first()

    def delete_user(self, user_id):
        user = self.get_user_by_uuid(user_id)
        user.deleted = True
        self.db.commit()