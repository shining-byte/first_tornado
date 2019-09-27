# -*- coding:utf-8 -*-
# Author: cmzz
# @Time :2019/8/22
import base64
import json
import struct
from datetime import datetime
import functools
import re

from uuid import uuid4

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen, web, iostream, httpserver
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from tornado.options import define, options
from tornado.platform.asyncio import AsyncIOMainLoop
from paho.mqtt.client import Client
import paho.mqtt.client as mqtt
import peewee_async

from tornado_model import User, LoraDevice, WifiDevice


class SendDataToWifi(web.RequestHandler):
    async def post(self):
        send_data = self.get_argument('send_data')
        try:
            send_data = eval(send_data)
            if isinstance(send_data, dict):
                global TCP_CONNECTION
                if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                    await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                        bytes(str(send_data), encoding='utf-8'))
                    return_data = {'status': 200, 'message': 'success'}
                    self.write(json.dumps(return_data))
                # elif re.match(r"\w+", send_data['device_name']).group() in TCP_CONNECTION.keys():
                #     device_name = re.match(r"\w+", send_data['device_name']).group()
                #     await TCP_CONNECTION[device_name].write(bytes(str(send_data), encoding='utf-8'))
                #     return_data = {'status': 200, 'message': 'success'}
                #     self.write(json.dumps(return_data))
                else:
                    return_data = {'status': 500, 'message': 'failure, 设备TCP未连接'}
                    self.write(json.dumps(return_data))
            else:
                return_data = {'status': 500, 'message': 'failure, 命令有误'}
                self.write(json.dumps(return_data))
        except Exception as e:
            return_data = {'status': 500, 'message': 'failure, track:{}'.format(e)}
            #
            # del TCP_CONNECTION[send_data['device_name']]
            self.write(json.dumps(return_data))


class Test(web.RequestHandler):
    async def post(self):
        # global TCP_CONNECTION
        # data = self.get_arguments("data")
        offlamp = self.get_arguments("off-lamp")
        off1 = self.get_arguments("off-fan-1")
        off2 = self.get_arguments("off-fan-2")
        off3 = self.get_arguments("off-fan-3")

        on = self.get_arguments("on-lamp")
        on1 = self.get_arguments("on-fan-1")
        on2 = self.get_arguments("on-fan-2")
        on3 = self.get_arguments("on-fan-3")
        if (offlamp):
            send_data = '''{'device_name': 'fan-lamp', 'class': 'G406', 'lamp-1': '0', 'lamp-2': '0','lamp-3': '0'}'''
            try:
                send_data = eval(send_data)
                if isinstance(send_data, dict):
                    if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                        await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                            bytes(str(send_data), encoding='utf-8'))
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
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        elif (off1):
            send_data = '''{'device_name': 'fan-lamp', 'class': 'G406', 'fan-1': '0'}'''
            try:
                send_data = eval(send_data)
                if isinstance(send_data, dict):
                    if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                        await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                            bytes(str(send_data), encoding='utf-8'))
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
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        elif (off2):
            send_data = '''{'device_name': 'fan-lamp', 'class': 'G406', 'fan-2': '0'}'''
            try:
                send_data = eval(send_data)
                if isinstance(send_data, dict):
                    if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                        await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                            bytes(str(send_data), encoding='utf-8'))
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
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        elif (off3):
            send_data = '''{'device_name': 'fan-lamp', 'class': 'G406', 'fan-3': '0'}'''
            try:
                send_data = eval(send_data)
                if isinstance(send_data, dict):
                    if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                        await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                            bytes(str(send_data), encoding='utf-8'))
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
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        elif (on):
            send_data = '''{'device_name': 'fan-lamp', 'class': 'G406', 'lamp-1': '1', 'lamp-2': '1','lamp-3': '1'}'''
            try:
                send_data = eval(send_data)
                if isinstance(send_data, dict):
                    if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                        await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                            bytes(str(send_data), encoding='utf-8'))
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
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        elif (on1):
            send_data = '''{'device_name': 'fan-lamp', 'class': 'G406', 'fan-1': '2'}'''
            try:
                send_data = eval(send_data)
                if isinstance(send_data, dict):
                    if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                        await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                            bytes(str(send_data), encoding='utf-8'))
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
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        elif (on2):
            send_data = '''{'device_name': 'fan-lamp', 'class': 'G406', 'fan-2': '2'}'''
            try:
                send_data = eval(send_data)
                if isinstance(send_data, dict):
                    if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                        await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                            bytes(str(send_data), encoding='utf-8'))
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
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        elif (on3):
            send_data = '''{'device_name': 'fan-lamp', 'class': 'G406', 'fan-3': '2'}'''
            try:
                send_data = eval(send_data)
                if isinstance(send_data, dict):
                    if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                        await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                            bytes(str(send_data), encoding='utf-8'))
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
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        # self.write({'status':200, 'message':'success'})


class IndexHandler(web.RequestHandler):
    async def get(self):
        if database.is_closed():
            database.connect()
        try:
            # self.prepare()
            obj = await self.application.objects.create_or_get(LoraDevice, device_name='3634374710300059')
            devices = WifiDevice.select()
            # device_status = await self.application.objects.count(WifiDevice, device_name='fan-lamp')
            # print(device_status)
            # for i in device_status:
            #     print(i)
            # if(obj.data):
            await self.render("index.html", temperature=obj.data[0:5],
                              data2=DATA2, humidity=obj.data[5:10], date=obj.date, device_status=devices)
            await self.on_finish()
            # else:
            #     await self.render("index.html", temperature=0, data2=0, humidity=0, date=0, device_status=device_status)
        except Exception as e:
            await self.render("index.html", temperature=0,
                              data2=0, humidity=0, date=0, devices=devices)
            await self.on_finish()

    def prepare(self):
        database.connect(reuse_if_open=True)
        return super(IndexHandler, self).prepare()

    def on_finish(self):
        if not database.is_closed():
            database.close()
        return super(IndexHandler, self).on_finish()


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
        # print(DATA)
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
        info_dict = {}
        try:
            while True:
                msg = await stream.read_bytes(1024, partial=True)

                msg = eval(msg.decode('utf-8'))
                # print(msg, 'from', address[1])
                # 判断是否为初次建立连接,发送heartbeat
                # 用规定的指令设备名和课室创建key
                msg['port'] = address[1]

                if (msg['device_name'] in info_dict.keys()):  # 判断是否已经连接

                    if (info_dict[msg['device_name']] == msg):  # 判断是否心跳包
                        # print(info_dict[msg['device_name']])
                        print('状态相同,心跳包')
                    else:
                        # 下发指令或者android更改设备状态返回信息
                        print('更新操作')
                        if (msg['device_name'] == 'fan-lamp'):
                            match_list = re.findall('\w*-\d', str(msg))
                            print('回复指令', msg)
                            # print('re匹配字符串',match_list)
                            for i in match_list:
                                update = WifiDevice.update(status=msg[i]). \
                                    where(
                                    (WifiDevice.device_number == i) & (WifiDevice.class_number == msg['class']))
                                update.execute()
                        elif (msg['device_name'] == 'air'):
                            if ('degree' in msg.keys()):
                                update = WifiDevice.update(degree=msg['degree'], ). \
                                    where(
                                    (WifiDevice.device_name == msg['device_name']) & (
                                            WifiDevice.class_number == msg['class']))
                                update.execute()
                            elif ('status' in msg.keys()):
                                update = WifiDevice.update(status=msg['status'], ). \
                                    where(
                                    (WifiDevice.device_name == msg['device_name']) & (
                                            WifiDevice.class_number == msg['class']))
                                update.execute()
                            elif ('degree' in msg.keys()):
                                update = WifiDevice.update(degree=msg['degree'], ). \
                                    where(
                                    (WifiDevice.device_name == msg['device_name']) & (
                                            WifiDevice.class_number == msg['class']))
                                update.execute()
                            elif ('gear' in msg.keys()):
                                update = WifiDevice.update(gear=msg['gear'], ). \
                                    where(
                                    (WifiDevice.device_name == msg['device_name']) & (
                                            WifiDevice.class_number == msg['class']))
                                update.execute()
                            elif ('model' in msg.keys()):
                                update = WifiDevice.update(gear=msg['model'], ). \
                                    where(
                                    (WifiDevice.device_name == msg['device_name']) & (
                                            WifiDevice.class_number == msg['class']))
                                update.execute()
                        # 更新info_dict信息
                        info_dict[msg['device_name']] = msg
                        # print(info_dict)
                else:
                    print('第一次连接')
                    return_dict = {}
                    info_dict[msg['device_name']] = msg
                    TCP_CONNECTION[msg['device_name'] + msg['class']] = stream
                    # stream.write(bytes(msg, encoding='utf-8'))
                    # print(info_dict)
                    # if(device_name == 'lamp'):
                    if ('lamp' and 'fan' in msg.keys()):
                        print('同时存在')
                        for i in range(1, int(msg['fan']) + 1):
                            fan = WifiDevice.get_or_create(device_number='fan-{}'.format(i),
                                                           class_number=msg['class'],
                                                           defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                     'port': msg['port']})
                            return_dict['fan-{}'.format(i)] = fan[0].status
                        for j in range(1, int(msg['lamp']) + 1):
                            lamp = WifiDevice.get_or_create(device_number='lamp-{}'.format(j),
                                                            class_number=msg['class'],
                                                            defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                      'port': msg['port']})
                            return_dict['lamp-{}'.format(j)] = lamp[0].status
                    elif ('fan' in msg.keys()):
                        print('fan存入数据库操作')
                        for i in range(1, int(msg['fan']) + 1):
                            fan = WifiDevice.get_or_create(device_number='fan-{}'.format(i),
                                                           class_number=msg['class'],
                                                           defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                     'port': msg['port']})
                            return_dict['fan-{}'.format(i)] = fan[0].status
                            print(fan[0].status)
                            print(msg.keys())
                    elif ('lamp' in msg.keys()):
                        print('lamp存入数据库')
                        for j in range(1, int(msg['lamp']) + 1):
                            lamp = WifiDevice.get_or_create(device_number='lamp-{}'.format(j),
                                                            class_number=msg['class'],
                                                            defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                      'port': msg['port']})
                            return_dict['lamp-{}'.format(j)] = lamp[0].status

                    elif ('air' in msg.keys()):
                        print('空调')
                        for k in msg['air']:
                            air = WifiDevice.get_or_create(device_name='air-{}'.format(k),
                                                           class_number=msg['class'],
                                                           defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                     'port': msg['port']})
                            return_dict['air-{}'.format(k)] = air[0].status
                    return_dict['device_name'] = msg['device_name']
                    return_dict['class'] = msg['class']
                    # 硬件死机重连返回必要信息
                    print('return_dict{}-----------------------'.format(return_dict))
                    await stream.write(bytes(str(return_dict), encoding='utf-8'))
                    del return_dict
                    # 重连修改连接端口号
                    update = WifiDevice.update(port=msg['port'], is_alive=1).where(
                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                    update.execute()
        except StreamClosedError as e:
            # 掉线处理
            for value in info_dict.values():
                # value = eval(value)
                if (address[1] in value.values()):
                    # print(value['device_name'], value['class'])
                    # wifi设备掉线,数据更改数据库设备状态
                    update = WifiDevice.update(is_alive=0).where(WifiDevice.port == address[1])
                    update.execute()
                    # print(value.values())
            # wifi tcp断开后会出错, 根据address查询数据库并修改状态
            print('设备掉线处理,错误信息{}'.format(e))
            # print("TcpHandler---------{}".format(e))


async def heartbeat():
    try:
        for key, value in TCP_CONNECTION.items():
            print('{}发送心跳包'.format(key))
            await value.write(b"{'heartBeat'}")
            # await i.write(b"heartBeat")
    except Exception as e:
        TCP_CONNECTION.pop(key)

        print('出错设备号{},错误信息{}'.format(key, e))


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
database = peewee_async.MySQLDatabase('tornado_db',
                                      **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost',
                                         'port': 3306, 'user': 'tornado_user', 'password': 'ciel2019'})
# database.set_allow_sync(False)

define("port", default=9004, help="run on the given port", type=int)
settings = {'debug': True, 'template_path': 'templates', 'static_path': "static", "xsrf_cookies": True}
AsyncIOMainLoop().install()
app = web.Application(
    handlers=[
        (r"/wifi", SendDataToWifi),
        (r"/mqtt", GetMqttData),
        # (r"/api/users/", GetAllUserHandler),
        (r"/user", GetUserHandler),
        (r"/", IndexHandler),
        (r"/test", Test)
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

