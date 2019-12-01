from handlers.base import BaseHandler
from tornado.web import authenticated
from tornado.web import MissingArgumentError
from models.smartroom import *
from service.device_connection import TCP_CONNECTION
from config import code
import json


class LoginHandler(BaseHandler):
    def get(self):
        # 未登录则发送未登录消息
        self.write({
            'code': code["unlogin"],
            "msg": "请先登录"
        })

    # 登录方法
    async def post(self):
        try:
            # 参数不存在产生MissingArgumentError
            account = self.get_argument("account")
            passwd = self.get_argument("passwd")
            # 参数空或不存在都归为MissingArgumentError
            if (account == None or passwd == None):
                raise MissingArgumentError
            teacher = await self.application.objects.get(Teacher, account=account, passwd=passwd)

            # 设置登录session
            session=self.get_session()
            session["teacher"]=teacher

            self.write({
                "code":code["success"],
                "name":teacher.name,
                "href":"/"
            })

        except Teacher.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "账户或密码不存在"
            })
        except MissingArgumentError:
            self.write({
                "code": code["empty"],
                "msg": "参数缺少"
            })


class LogoutHandler(BaseHandler):
    @authenticated
    def get(self):
        self.get_session().clear_session()
        self.write({
            "code": code["success"]
        })




