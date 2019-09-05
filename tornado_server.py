# -*- coding:utf-8 -*-
# Author: cmzz
# @Time :2019/8/22
import base64
import json
import struct
from datetime import datetime
import functools
from uuid import uuid4

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen, web, iostream, httpserver
from tornado.tcpserver import TCPServer
from tornado.options import define, options
from tornado.platform.asyncio import AsyncIOMainLoop
from paho.mqtt.client import Client
import paho.mqtt.client as mqtt
import peewee_async

from tornado_model import User, WifiDevice, LoraDevice


class SendDataToWifi(web.RequestHandler):
    async def post(self):
        send_data = self.get_argument('send_data')
        try:
            send_data = eval(send_data)
            if isinstance(send_data, dict):
                global TCP_CONNECTION
                if send_data['device_name'] in TCP_CONNECTION.keys():
                    await TCP_CONNECTION[send_data['device_name']].write(bytes(str(send_data), encoding='utf-8'))
                    return_data = {'status': 200, 'message': 'success'}
                    self.write(json.dumps(return_data))
                else:
                    return_data = {'status': 500, 'message': 'failure, 设备TCP未连接'}
                    self.write(json.dumps(return_data))
            else:
                return_data = {'status': 500, 'message': 'failure, 命令有误'}
                self.write(json.dumps(return_data))
        except Exception as e:
            return_data = {'status': 500, 'message': 'failure, track:{}'.format(e)}
            self.write(return_data)


class IndexHandler(web.RequestHandler):
    async def get(self):
        obj = await self.application.objects.get(LoraDevice, device_name='3634374710300059')
        await self.render("index.html", temperature=obj.data[0:5],
                          data2=DATA2, humidity=obj.data[5:10], date=obj.date)


class GetMqttData(web.RequestHandler):
    def post(self):
        send_data = self.get_argument('send_data')
        status = send_mqtt(send_data)
        if status:
            self.set_status(200)


class Mqtt(Client):
    def on_connect(self, client, userdata, flags, rc):
        # 初始化DATA
        global DATA
        DATA = 'None'
        client.subscribe("application/1/device/3634374710300059/rx")

    def on_message(self, client, userdata, msg):
        global DATA
        DATA = json.loads(msg.payload)
        print(DATA)
        if isinstance(DATA, dict):
            DATA = base64.b64decode(DATA['data'])


class Mqtt2(Client):
    def on_connect(self, client, userdata, flags, rc):
        # 初始化DATA2
        global DATA2
        DATA2 = 'None'
        client.subscribe("application/1/device/36343747104a002e/rx")

    def on_message(self, client, userdata, msg):
        global data2
        data2 = json.loads(msg.payload)
        if isinstance(data2, dict):
            data2 = base64.b64decode(data2['data']).hex().upper()


class GetAllUserHandler(web.RequestHandler):
    async def get(self):
        count = await self.application.objects.count(query=User.select())
        query_list = []
        for i in range(1, count + 1):
            query_dict = {}
            users = await self.application.objects.get(User, id=i)
            query_dict['username'] = users.username
            query_dict['password'] = users.password
            query_dict['is_admin'] = users.is_admin
            query_dict['sign_date'] = str(users.sign_date)
            query_list.append(query_dict)
        reslut = {}
        reslut['data'] = query_list
        await self.write(reslut)


class GetUserHandler(web.RequestHandler):
    async def get(self):
        userid = self.get_argument('id', None)
        if not userid:
            self.write("Please provide the 'id' query argument ")
            return
        try:
            obj = await self.application.objects.get(User, id=userid)
            self.write({
                'id': obj.id,
                'name': obj.username,
                'password': obj.password,
                'is_admin': obj.is_admin,
                'sign_date': obj.sign_date,
            })
        except Exception as e:
            raise web.HTTPError(404, "objects not found, error:{}".format(e))


class TcpHandler(TCPServer):
    global TCP_CONNECTION

    async def handle_stream(self, stream, address):
        global FLAG
        try:
            while True:
                msg = await stream.read_bytes(1024, partial=True)
                FLAG = True
                # print(msg, 'from', address)
                msg = eval(msg.decode('utf-8'))
                TCP_CONNECTION[msg['device_name']] = stream
                # if msg == 'over':
                #     stream.close()
        # except iostream.StreamClosedError:
        except Exception as e:
            print(e)
            FLAG = False

            # pass


async def heartbeat():
    if FLAG is True:
        for i in TCP_CONNECTION.values():
            await i.write(b'heartBeat')
    else:
        print('tcp心跳包-----{}'.format(datetime.now()))


def send_mqtt(data):
    HOST = "127.0.0.1"
    PORT = 1883
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    # test(client)
    str_data = base64.b64encode(bytes(data, encoding='utf-8')).decode('utf-8')

    param = '''{"reference": "abcd1234", "confirmed": false, "fPort": 100, "data": "%s"}''' % (str_data)
    # print(param)
    client.publish("application/1/device/36343747104a002e/tx", param, 2)
    print(datetime.now())
    client.loop_start()
    return True


# 定时保存mqtt数据


def save_mqtt_data():
    global DATA
    if isinstance(DATA, str):
        print('数据为空')
        pass
    else:
        temperature = str(struct.unpack('!f', DATA[0:4])[0])[:5]
        humidity = str(struct.unpack('!f', DATA[4:8])[0])[:5]
        # print(DATA)
        q = (LoraDevice.update({LoraDevice.data: temperature + humidity, LoraDevice.date: datetime.now()}).where(
            LoraDevice.device_name == '3634374710300059'))
        q.execute()
        # app.objects.create(LoraDevice, device_name='3634374710300059', data=DATA)
        del DATA

    # 全局变量


TCP_CONNECTION = {}
FLAG = False
database = peewee_async.PooledMySQLDatabase('tornado_db',
                                            **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost',
                                               'port': 3306, 'user': 'tornado_user', 'password': 'ciel2019'})
define("port", default=9999, help="run on the given port", type=int)
settings = {'debug': True, 'template_path': 'templates', 'static_path': "static", "xsrf_cookies": True}
AsyncIOMainLoop().install()
app = web.Application(
    handlers=[
        (r"/wifi", SendDataToWifi),
        (r"/mqtt", GetMqttData),
        # (r"/api/users/", GetAllUserHandler),
        (r"/user", GetUserHandler),
        (r"/", IndexHandler)
    ],
    **settings
)
app.objects = peewee_async.Manager(database=database)
if __name__ == "__main__":
    # app.objects.allow_sync = False
    # app.objects
    options.parse_command_line()

    server = TcpHandler()
    server.listen(23333)
    server.start()
    PeriodicCallback(functools.partial(heartbeat), callback_time=10000).start()  # start scheduler 每隔10s执行一次发送心跳包

    # 获取59数据
    client = Mqtt()
    client.connect("127.0.0.1", 1883, 60)  # 服务器上IP改为127.0.0.1即可 端口为设定的1883
    client.user_data_set("test")
    client.loop_start()
    # 获取2e数据
    client2 = Mqtt2()
    client2.connect("127.0.0.1", 1883, 60)  # 服务器上IP改为127.0.0.1即可 端口为设定的1883
    client2.user_data_set("test")
    client2.loop_start()

    # client3 = mqtt.Client()
    # client3.connect('127.0.0.1', 1883, 60)

    # 下发2e数据
    # PeriodicCallback(functools.partial(send_mqtt, '11223344'), callback_time=1000).start()

    # 定时保存59设备数据,
    PeriodicCallback(functools.partial(save_mqtt_data), callback_time=300000).start()
    '''
    # 定时器传参数 use a lambda or functools.partial.
    PeriodicCallback(functools.partial(TcpHandler.heartbeat, 1), callback_time=30000).start()   #每隔30s执行一次发送心跳包
    x = 1
    y = 2 
    periodic_callback = PeriodicCallback(
        lambda: my_function(x, y),
        10)
    '''
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    http_server.start()
    IOLoop.instance().start()

