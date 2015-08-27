#coding=utf-8
__author__ = 'wan'
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql.functions import now
from common.base import BaseModel


class UserDO(BaseModel):
    """
    用户表
    """
    __tablename__ = 'my_user'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=True)
    user_name = Column(String(128), nullable=True)
    user_pwd = Column(String(128), nullable=True)
    sex = Column(String(10), nullable=True)
    phone = Column(String(15), nullable=True)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    avatar = Column(String(128), doc='头像')

    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=False)

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column in ['gmt_created', 'gmt_modified', 'deleted']:
                continue
            d[column.name] = getattr(self, column.name)
        return d


class ChatLogDO(BaseModel):
    """ 聊天记录表 """
    __tablename__ = 'my_chat_log'
    id = Column(Integer, primary_key=True)
    from_user = Column(String(50), nullable=True)
    to_user = Column(String(50))
    sendtime = Column(String(50), nullable=True)
    content = Column(String(500), nullable=True)

    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=False)

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column in ['gmt_created', 'gmt_modified', 'deleted']:
                continue
            d[column.name] = getattr(self, column.name)
        return d

