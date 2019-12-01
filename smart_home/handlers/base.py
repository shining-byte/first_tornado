
import base64,uuid
from service.singlemode import Singleton
from tornado.web import RequestHandler
from config import  logging

# 目前缺陷，没有会话过期清除机制
session={}
class BaseHandler(RequestHandler):
    def get_current_user(self):
        # 判断teacher是否存在，存在则以登录,不存在返回None
        self.teacher=self.get_session()["teacher"]
        if self.teacher:
            return True
        else:
            return False

    def get_session(self):
        return self.Session(self)

    class Session:
        def __init__(self, handler):
            self.handler = handler
            self.expireday = 7  #过期时间
            self.user_cookie=None   #sessioncookie

            clientcookie=handler.get_secure_cookie("session")
            # 判断有无session，有就用客户端的cookie，没有就发放一个
            if clientcookie==None:
                cookie = bytes.decode(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))
                handler.set_secure_cookie("session",cookie,self.expireday)
                self.user_cookie=cookie
            else:
                self.user_cookie = bytes.decode(clientcookie)

            # 如果不存在session不存在该cookie就新建一个
            if not session.get(self.user_cookie):
                session[self.user_cookie] = {}

        def __setitem__(self, key, value):
            session[self.user_cookie][key]=value

        def __getitem__(self, item):
            # 不存在返回None
            logging.info("session"+str(self.user_cookie))
            return session[self.user_cookie].get(item)

        def clear_session(self):
            self.handler.clear_cookie("session")
            del session[self.user_cookie]
