#coding=utf-8
__author__ = 'wan'
from models.user_do import UserDO
from sqlalchemy import and_, desc, func

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
            self.db.add(user_do)
            self.db.commit()
            return True, ''
        except Exception, e:
            log.error(e)
            return False, e

    def get_user_by_id(self, id):
        return self.get_query.filter_by(and_(id=id, deleted=False)).first()

    def get_user_by_uuid(self, user_id):
        return self.get_query.filter(and_(UserDO.user_id==user_id, UserDO.deleted==0)).first()

    def delete_user(self, user_id):
        user = self.get_user_by_uuid(user_id)
        user.deleted = True
        self.db.commit()

    def get_user_by_name_and_pwd(self, name, pwd):
        user = self.get_query.filter_by(user_name=name, user_pwd=pwd, deleted=False).first()
        if not user:
            return False, ''
        return True, user

    def get_all_user_by_order(self):
        return self.get_query.order_by(desc(UserDO.is_active)).all()

    def get_user_count(self):
        return self.db.query(UserDO.user_id).count()

    def get_user_count_by_active(self):
        return self.db.query(func.count('*')).filter(UserDO.is_active==True).scalar()
