#coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.config import DB_CONNECT_STRING
from tornado import web
from sqlalchemy.ext.declarative import declarative_base
from common.redis_cache import RedisCacheManager


BaseModel = declarative_base()

def connect_db():
    engine = create_engine(DB_CONNECT_STRING, echo=False)
    session = sessionmaker(bind=engine)
    db = session()
    return db

DB = connect_db()

class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def get_current_user(self):
        return self.get_secure_cookie('user_id')


class Application(web.Application):
    def __init__(self, handlers, **settings):
        super(Application, self).__init__(handlers, **settings)
        self.db = DB
        self.redis = RedisCacheManager()._con






