#coding=utf-8
from common.base import BaseHandler
from services.admin.user_service import UserService
import hashlib


class LoginHandler(BaseHandler):

    def get(self):
        return self.render('login.html')

    def post(self):
        pass


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




