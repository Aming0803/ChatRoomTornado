#coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.config import DB_CONNECT_STRING
from tornado import web
from sqlalchemy.ext.declarative import declarative_base
from common.redis_cache import RedisCacheManager


BaseModel = declarative_base()


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

class Application(web.Application):
    def __init__(self, handlers, **settings):
        super(Application, self).__init__(handlers, **settings)
        engine = create_engine(DB_CONNECT_STRING, echo=True)
        db_session = sessionmaker(bind=engine)
        self.db = db_session()
        self.redis = RedisCacheManager()._con


