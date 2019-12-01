import os
import logging

from peewee_async import MySQLDatabase


port=9004
BASE_DIR=os.path.dirname(__file__)
database = MySQLDatabase('tornado_db', **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'port': 3306,
                                          'user': 'tornado_user', 'password': 'ciel2019'})
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                     # filename='tornado.log',
                     # filemode='w'
                    )
# logger = logging.getLogger(__name__)
#
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# console.setLevel(20)
# console_formatter = logging.Formatter('%(asctime)s - %(filename)s - [line]:%(lineno)d - %(levelname)s - %(message)s')
# console.setFormatter(console_formatter)
# logger.addHandler(console)

# 上课时间和下课时间
session_time={
    "start":{
        1: [7, 50],
        3:[9,50],
        5:[14,20],
        7:[16,10],
        9:[19,30]
    },
    "end":{
        1: [9, 30],
        3:[11,40],
        5:[16,10],
        7:[17,50],
        9: [21, 20]
    }
}

#返回代码
code={
    "fail":0,
    "success":1,
    "unlogin":2,
    "empty":3
}

setting={
    "static_path":os.path.join(BASE_DIR,"static"),
    "template_path": os.path.join(BASE_DIR, "template"),
    "cookie_secret": "q+KNs2/1TnihOj9YzGON1V8KXw74mE2qngZ5MDG29Vw=",
    "login_url":"/login",
    "debug": True,
    # "xsrf_cookies": False
}