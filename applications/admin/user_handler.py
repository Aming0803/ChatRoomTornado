#coding=utf-8
from common.base import BaseHandler
from services.admin.user_service import UserService
from common.redis_cache import RedisCacheManager
import hashlib


class IndexHandler(BaseHandler):
    def get(self):
        return self.redirect('/login')


class LoginHandler(BaseHandler):

    def get(self):
        return self.render('login.html')

    def post(self):
        user_name = self.get_argument('user_name', None)
        user_pwd = self.get_argument('user_pwd', None)

        if not user_name or not user_pwd:
            msg = u'用户名或密码不能为空'
            return self.render('login.html', msg=msg)

        user_pwd = hashlib.md5(user_pwd).hexdigest()

        success, user = self.get_user_by_name_and_pwd(user_name, user_pwd)
        if not success:
            return self.render('login.html', msg=u'用户不存在')

        user.is_active = True
        self.db.commit()

        self.incr_active_count()
        self.make_cookies(user)

        return self.redirect('/chat')

    def get_user_by_name_and_pwd(self, user_name, user_pwd):
        user_ser = UserService(self.db)
        return user_ser.get_user_by_name_and_pwd(user_name, user_pwd)

    def make_cookies(self, user):
        self.set_secure_cookie('user_id', user.user_id)

    def incr_active_count(self):
        redis_ser = RedisCacheManager()

        if not redis_ser.get('active_count'):
            redis_ser.set('active_count', self.get_active_user_count())

        redis_ser.incr('active_count')

    def get_active_user_count(self):
        user_ser = UserService(self.db)
        return user_ser.get_user_count_by_active()


class RegisterHandler(BaseHandler):

    def get(self):
        return self.render('register.html')

    def post(self):
        user_name = self.get_argument('user_name', None)
        user_pwd = self.get_argument('user_pwd', None)
        re_pwd = self.get_argument('re_pwd', None)
        phone = self.get_argument('phone', None)
        sex = self.get_argument('sex', None)
        avatar = self.get_argument('avatar', None)
        #此处偷懒了，没有在后台验证
        user_pwd = hashlib.md5(user_pwd).hexdigest()
        success, msg = self.create_user(user_name=user_name, user_pwd=user_pwd, phone=phone, sex=sex, avatar=avatar)
        if not success:
            return self.write('sorry,注册失败!')


        return self.redirect(self.get_login_url())

    def create_user(self, **kwargs):
        user_ser = UserService(self.db)
        return user_ser.create_user(kwargs)

    def incr_total_count(self):
        redis_ser = RedisCacheManager()

        if not redis_ser.get('total_count'):
            redis_ser.set('total_count', self.get_total_count())

        redis_ser.incr('total_count')

    def get_total_count(self):
        user_ser = UserService(self.db)
        return user_ser.get_user_count()


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user_id')
        return self.redirect(self.get_login_url())



