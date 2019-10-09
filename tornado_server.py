# -*- coding:utf-8 -*-
# Author: cmzz
# @Time :2019/8/22
import base64
import json
import struct
from datetime import datetime
import functools
import re
import logging
import random
import string
from uuid import uuid4

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen, web, iostream, httpserver,auth
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from tornado.options import define, options
from tornado.platform.asyncio import AsyncIOMainLoop
from paho.mqtt.client import Client
import paho.mqtt.client as mqtt
import peewee_async

from tornado_model import User, LoraDevice, WifiDevice
from TmallDeivces import devices

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='tornado.log',
                    filemode='w')


class IndexHandler(web.RequestHandler):
    """
    初始页面
    """
    async def get(self):
            obj = await self.application.objects.create_or_get(LoraDevice, device_name='3634374710300059')
            devices = WifiDevice.select()
            await self.render("index.html", temperature=obj[0].data[0:5],
                              data2=0, humidity=obj[0].data[5:10], date=obj[0].date, devices=devices)
    def prepare(self):
        database.connect()
        return super(IndexHandler, self).prepare()

    def on_finish(self):
        if not database.is_closed():
            database.close()
        return super(IndexHandler, self).on_finish()


class TcpHandler(TCPServer):
    """
    tcp 连接
    """
    global TCP_CONNECTION

    async def handle_stream(self, stream, address):
        info_dict = {}
        try:
            while True:
                msg = await stream.read_bytes(2048, partial=True)
                print(msg)
                # logging.info('记录tcp连接:{}'.format(msg))
                msg = msg.decode('utf-8')
                # logging.info('msg1{}'.format(msg))
                for msg in re.findall('({.*?})', msg):
                    msg = eval(msg)
                    logging.info('msg{}'.format(msg))
                    # 掉线处理要用到的port
                    msg['port'] = address[1]
                    # 判断是否为初次建立连接,发送heartbeat
                    # 用规定的指令设备名和课室创建key
                    # 处理返回指令
                    if(msg['device_name']+msg['class'] in info_dict.keys()):  # 判断是否已经连接,这里匹配，应该为 {'device_name': 'fan-lamp-curtain', 'class': 'G511', 'fan': '3', 'lamp': '3', 'curtain': '1'}
                        # info_dict根据device_name和class来存放整一个msg
                        if (msg == info_dict[msg['device_name']+msg['class']]):  # 判断是否心跳包
                            # print(info_dict[msg['device_name']])
                            print('状态相同,心跳包')
                            logging.info('心跳包')
                            continue
                        else:
                            # 下发指令或者android更改设备状态返回信息
                            # logging.info('更新操作{}'.format(msg))
                            print('更新操作')
                            if (msg['device_name'] == 'fan-lamp-curtain'):

                                match_list = re.findall('\w*-\d', str(msg))
                                # 匹配lamp-1,fan-1...
                                for i in match_list:
                                    update = WifiDevice.update(status=msg[i]). \
                                        where(
                                        (WifiDevice.device_number == i) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # 更新info_dict信息里面单个信息
                                    info_dict[msg['device_name']+msg['class']][i] = msg[i] # msg[i] 为lamp-1的 ‘1’ or ‘0’
                            elif (re.findall('air', msg['device_name'])):
                                # logging.info('air{}'.format(msg))
                                # logging.info('info_dict{}'.format(info_dict[msg['device_name']]))
                                if ('degree' in msg.keys() and 'status' in msg.keys() and 'gear' in msg.keys() and 'model' in msg.keys()):
                                    logging.info('更新全部')
                                    # logging.info(msg)
                                    update = WifiDevice.update(degree=msg['degree'], status=msg['status'], gear=msg['gear'], model=msg['model']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    info_dict[msg['device_name']+msg['class']]['degree'] = msg['degree']
                                    info_dict[msg['device_name']+msg['class']]['status'] = msg['status']
                                    info_dict[msg['device_name']+msg['class']]['gear'] = msg['gear']
                                    info_dict[msg['device_name']+msg['class']]['model'] = msg['model']
                                # 单独更新
                                elif('degree' in msg.keys()):
                                    update = WifiDevice.update(degree=msg['degree']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # logging.info('更新degree')
                                    info_dict[msg['device_name']+msg['class']]['degree'] = msg['degree']
                                elif ('status' in msg.keys()):
                                    update = WifiDevice.update(status=msg['status']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # logging.info('更新status')
                                    info_dict[msg['device_name']+msg['class']]['status'] = msg['status']
                                elif ('gear' in msg.keys()):
                                    update = WifiDevice.update(gear=msg['gear']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # logging.info('更新gear')
                                    info_dict[msg['device_name']+msg['class']]['gear'] = msg['gear']
                                elif ('model' in msg.keys()):
                                    update = WifiDevice.update(gear=msg['model']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # logging.info('更新model')
                                    info_dict[msg['device_name']+msg['class']]['model'] = msg['model']
                    else:
                        print('第一次连接')
                        # logging.info('第一次连接')
                        return_dict = {}
                        TCP_CONNECTION[msg['device_name'] + msg['class']] = stream
                        # stream.write(bytes(msg, encoding='utf-8'))
                        # 根据初次连接上发的指令，记录到数据库
                        if ('lamp' and 'fan' and 'curtain' in msg.keys()):
                            print('同时存在')
                            for i in range(1, int(msg['fan']) + 1):
                                fan = WifiDevice.get_or_create(device_number='fan-{}'.format(i),
                                                               class_number=msg['class'],
                                                               defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                         'port': address[1]})
                                return_dict['fan-{}'.format(i)] = fan[0].status
                            for j in range(1, int(msg['lamp']) + 1):
                                lamp = WifiDevice.get_or_create(device_number='lamp-{}'.format(j),
                                                                class_number=msg['class'],
                                                                defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                          'port': address[1]})
                                return_dict['lamp-{}'.format(j)] = lamp[0].status
                            for k in range(1, int(msg['curtain']) + 1):
                                curtain = WifiDevice.get_or_create(device_number='curtain-{}'.format(k),
                                                                   class_number=msg['class'],
                                                                   defaults={'device_name': msg['device_name'],
                                                                             'is_alive': 1,
                                                                             'port': address[1]})
                                return_dict['curtain-{}'.format(k)] = curtain[0].status
                        elif ('fan' in msg.keys()):
                            print('fan存入数据库操作')
                            for i in range(1, int(msg['fan']) + 1):
                                fan = WifiDevice.get_or_create(device_number='fan-{}'.format(i),
                                                               class_number=msg['class'],
                                                               defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                         'port': address[1]})
                                return_dict['fan-{}'.format(i)] = fan[0].status
                                print(fan[0].status)
                                print(msg.keys())
                        elif ('lamp' in msg.keys()):
                            print('lamp存入数据库')
                            for j in range(1, int(msg['lamp']) + 1):
                                lamp = WifiDevice.get_or_create(device_number='lamp-{}'.format(j),
                                                                class_number=msg['class'],
                                                                defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                          'port': address[1]})
                                return_dict['lamp-{}'.format(j)] = lamp[0].status

                        elif (re.findall('air', msg['device_name'])):
                            print('空调')
                            # number = re.findall('\d', msg['device_name'])[0]
                            # for k in msg['air']:
                            air = WifiDevice.get_or_create(device_name=msg['device_name'],
                                                           class_number=msg['class'],
                                                           defaults={'degree': '25', 'is_alive': 1, 'gear': '1',
                                                                     'model': '1',
                                                                     'port': address[1]})
                            return_dict['status'] = air[0].status
                            return_dict['degree'] = str(air[0].degree)
                            return_dict['gear'] = air[0].gear
                            return_dict['model'] = air[0].model
                            logging.info(air[0])
                            logging.info('空调----------', return_dict)
                        return_dict['device_name'] = msg['device_name']
                        return_dict['class'] = msg['class']
                        # logging.info('info_dict{}'.format(info_dict.values()))
                        # 硬件死机重连返回必要信息
                        print('return_dict:{}'.format(return_dict))
                        # await stream.write(b"{'heartBeat'}")
                        logging.info('return_dict{}'.format(return_dict))
                        await stream.write(bytes(str(return_dict), encoding='utf-8'))
                        return_dict['port'] = msg['port']
                        info_dict[msg['device_name']+msg['class']] = return_dict
                        del return_dict
                        # 重连修改连接端口号
                        update = WifiDevice.update(port=address[1], is_alive=1).where(
                            (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                        update.execute()
                    # else:
                    #     # 处理单片机返回非json数据
                    #     logging.info("处理单片机返回非json数据：{}".format(msg))
                    #     print(msg)
        except StreamClosedError:
            # 掉线处理
            for value in info_dict.values():
                # value = eval(value)
                if (address[1] in value.values()):
                    # print(value['device_name'], value['class'])
                    # wifi设备掉线,数据更改数据库设备状态
                    update = WifiDevice.update(is_alive=0).where(WifiDevice.port == address[1])
                    update.execute()
            # wifi tcp断开后会出错, 根据address查询数据库并修改状态
            print('掉线')
        except SyntaxError as e:
            print('错误信息{}'.format(e))
            # print("TcpHandler---------{}".format(e))


async def heartbeat():
    """
    心跳包
    :return:
    """
    try:
        for key, value in TCP_CONNECTION.items():
            print('{}发送心跳包'.format(key))
            logging.info('{}发送心跳包'.format(key))
            await value.write(b"{'heartBeat'}")
            # await i.write(b"heartBeat")
    except Exception as e:
        TCP_CONNECTION.pop(key)

        print('出错设备号{},错误信息{}'.format(key, e))


class SendDataToWifi(web.RequestHandler):
    """
    初始页面文本框下发指令
    """
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
    """
    index页面按钮下发指令
    """
    async def post(self):
        # global TCP_CONNECTION
        # data = self.get_arguments("data")
        offlamp = self.get_arguments("off-lamp")
        off1 = self.get_arguments("off-fan-1")
        off2 = self.get_arguments("off-fan-2")
        off3 = self.get_arguments("off-fan-3")
        off4 = self.get_arguments("off-curtain-1")

        stop = self.get_arguments("stop-curtain-1")

        on = self.get_arguments("on-lamp")
        on1 = self.get_arguments("on-fan-1")
        on2 = self.get_arguments("on-fan-2")
        on3 = self.get_arguments("on-fan-3")
        on4 = self.get_arguments("on-curtain-1")
        if (offlamp):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'lamp-1': '0', 'lamp-2': '0','lamp-3': '0'}'''
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
                self.write(return_data)
        elif (off1):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'fan-1': '0'}'''
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
        elif (off4):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'curtain-1': '0'}'''
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
        elif (stop):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'curtain-1': '2'}'''
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
        elif (on4):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'curtain-1': '1'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'fan-2': '0'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'fan-3': '0'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'lamp-1': '1', 'lamp-2': '1','lamp-3': '1'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'fan-1': '2'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'fan-2': '2'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'G406', 'fan-3': '2'}'''
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


class OAuth2Home(web.RequestHandler,  auth.OAuth2Mixin):
    """
    天猫精灵获取授权
    """
    _OAUTH_AUTHORIZE_URL = 'https://ciel.pub/OAuth2Home'
    # https://xxx.com/auth/authorize?redirect_uri=https%3A%2F%2Fopen.bot.tmall.com%2Foauth%2Fcallback%3FskillId%3D11111111%26token%3DXXXXXXXXXX&client_id=XXXXXXXXX&response_type=code&state=111
    # 验证天猫上精灵填写的client_id,
    async def get(self):
        if self.get_arguments('code'):
            # self.write({'code': self.get_argument('code'), 'url':self.get_argument('redirect_uri')})
            url = self.get_argument('redirect_uri')+"&code="+self.get_argument('code')+"&state="+self.get_argument('state')
            self.redirect(url=url)
        else:
            client_id = self.get_arguments('client_id')
            code = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            self.authorize_redirect(
                redirect_uri=self.get_argument('redirect_uri'),
                client_id=self.get_argument('client_id'),
                # scope=['profile', 'email'],
                response_type=self.get_argument('response_type'),
                extra_params={'state': self.get_argument('state'), 'code': code},
                # extra_params={'approval_prompt': 'auto'}
            )


class AccessTokenURL(web.RequestHandler):
    """
    天猫精灵获取access token
    """
    async def post(self):
        grant_type = self.get_argument('grant_type')

        if grant_type == 'refresh_token':
            # https://XXXXX/token?grant_type=refresh_token&client_id=XXXXX&client_secret=XXXXXX&refresh_token=XXXXXX
            logging.info('refresh_token')
            # 验证refresh_token
            access_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            refresh_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            data = {
              "access_token": access_token,
              "refresh_token": refresh_token,
              "expires_in": 3600,
              }
            self.write(data)
            print('refresh_token')
        elif grant_type == 'authorization_code':
            # https://XXXXX/token?grant_type=authorization_code&client_id=XXXXX&client_secret=XXXXXX&code=XXXXXXXX&redirect_uri=https%3A%2F%2Fopen.bot.tmall.com%2Foauth%2Fcallback
            code = self.get_argument('code')
            # 验证code的正确性
            access_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            refresh_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            data = {
              "access_token": access_token,
              "refresh_token": refresh_token,
              "expires_in": 3600,
              }
            self.write(data)


class RevTmCommand(web.RequestHandler):
    """
    天猫精灵post指令网关
    """
    async def post(self):
        global send_data
        dicts = eval(self.request.body.decode('utf-8'))
        if dicts['header']['namespace'] == "AliGenie.Iot.Device.Discovery":
            print('发现设备')
            # from TmallDevices import devices
            self.write(devices)
        elif dicts['header']['namespace'] == "AliGenie.Iot.Device.Control":
            name = dicts['header']['name']
            messageId = dicts['header']['messageId']
            deviceType = dicts['payload']['deviceType']
            deviceId = dicts['payload']['deviceId']
            send_data = {'device_name': 'fan-lamp-curtain', 'class': 'G406'}
            # logging.info('wdaadaaaaaa{}'.format(dicts))
            if name == 'TurnOn':
                print('开')
                if deviceType == 'fan':
                    send_data['fan-2'] = '1'
                elif deviceType == 'light':
                    send_data['lamp-1'] = '1'
                    send_data['lamp-2'] = '1'
                    send_data['lamp-3'] = '1'
                elif deviceType == 'sensor':
                    send_data['lamp-1'] = '1'
                    send_data['lamp-2'] = '1'
                    send_data['lamp-3'] = '1'
                    send_data['fan-2'] = '1'
                    send_data['curtain-1'] = '1'
                    send_data['curtain-2'] = '1'
            elif name == 'TurnOff':
                if deviceType == 'fan':
                    print('关')
                    send_data['fan-2'] = '0'
                elif deviceType == 'light':
                    send_data['lamp-1'] = '0'
                    send_data['lamp-2'] = '0'
                    send_data['lamp-3'] = '0'
                elif deviceType == 'sensor':
                    send_data['lamp-1'] = '0'
                    send_data['lamp-2'] = '0'
                    send_data['lamp-3'] = '0'
                    send_data['fan-2'] = '0'
                    send_data['curtain-1'] = '0'
                    send_data['curtain-2'] = '0'
            # try:
            send = {'device_name': 'fan-lamp-curtain', 'class': 'G406'}
            logging.info('send_data{}'.format(send_data))
            if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                await TCP_CONNECTION[send_data['device_name'] + send_data['class']].write(
                    bytes(str(send), encoding='utf-8'))
                return_data = {
                                  "header": {
                                      "namespace": "AliGenie.Iot.Device.Control",
                                      "name": "TurnOnResponse",
                                      "messageId": messageId,
                                      "payLoadVersion": 1
                                   },
                                   "payload": {
                                      "deviceId": deviceId
                                    }
                                }
                print('下发成功')
                self.write(return_data)
            else:
                return_data = {
                              "header": {
                                  "namespace": "AliGenie.Iot.Device.Control",
                                  "name": "ErrorResponse",
                                  "messageId": messageId,
                                  "payLoadVersion": 1
                               },
                               "payload": {
                                    "deviceId": deviceId,
                                     "errorCode": "DEVICE_NOT_SUPPORT_FUNCTION",
                                     "message": "设备tcp未连接"
                                }
                }
                print('下发失败')
                self.write(return_data)



class WebHook(web.RequestHandler):
    """
    天猫技能接口
    """
    async def post(self):
        return_dict = {
            "returnCode": "0",
            "returnErrorSolution": "",
            "returnMessage": "",
            "returnValue": {
                "reply": "好的",
                "resultType": "RESULT",
                "actions": [
                    {
                        "name": "audioPlayGenieSource",
                        "properties": {
                            "audioGenieId": "123"
                        }
                    }
                ],
                "properties": {},
                "executeCode": "SUCCESS",
                "msgInfo": ""
            }
        }
        get_json = self.request.body.decode('utf-8')
        logging.info(get_json)
        get_json = get_json.replace('true', '1')
        dicts = eval(get_json.replace('false', '0'))
        # print(/)
        if dicts['intentName'] == '参观':
            logging.info('参观')
            json_info = {'device_name': 'android', 'class': 'D712'}
            if json_info['device_name'] + json_info['class'] in TCP_CONNECTION.keys():
                logging.info('TCP_CONNECTION:{}'.format(TCP_CONNECTION))
                await TCP_CONNECTION[json_info['device_name'] + json_info['class']].write(
                    bytes(str('start'), encoding='utf-8'))
                # return_data['returnValue']['resultType'] = ''
                logging.info("好的{}".format(return_dict))
                self.write(return_dict)
            else:
                return_dict['returnValue']['reply'] = "安卓设备未连接"
                logging.info("安卓设备未连接{}".format(return_dict))
                self.write(return_dict)
        else:
            return_dict['returnValue']['reply'] = "非参观意图"
            logging.info('非{}'.format(return_dict))
            self.write(return_dict)


#  下面的都是lora的设备


class GetMqttData(web.RequestHandler):
    """
    lora设备下发指令
    """
    def post(self):
        send_data = self.get_argument('send_data')
        status = send_mqtt(send_data)
        if status:
            self.set_status(200)


class Mqtt(Client):
    """
    lora设备订阅，参考文档 https://blog.csdn.net/jiangjunjie_2005/article/details/96358863
    """
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
            # logging.info('mtqq59收到信息{}'.format(DATA))


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


def send_mqtt(data):
    """
    下发函数
    :param data:
    :return:
    """
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
    """
    保存lora设备数据
    :return:
    """
    global DATA
    if isinstance(DATA, str):
        print('数据为空')
        # logging.info('mqtt59数据为空')
        pass
    else:
        temperature = str(struct.unpack('!f', DATA[0:4])[0])[:5]
        humidity = str(struct.unpack('!f', DATA[4:8])[0])[:5]
        # print(DATA)
        # if(LoraDevice.get_or_create(device_number='3634374710300059',
        #                                                    defaults={'data': temperature+humidity})):
        q = (LoraDevice.update({LoraDevice.data: temperature + humidity, LoraDevice.date: datetime.now(), LoraDevice.is_alive: 1}).where(
            LoraDevice.device_name == '3634374710300059'))
        q.execute()
        # app.objects.create(LoraDevice, device_name='3634374710300059', data=DATA)
        del DATA
        # logging.info('mqtt59保存数据')

# 全局变量

TCP_CONNECTION = {}
database = peewee_async.MySQLDatabase('tornado_db',
                                      **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost',
                                         'port': 3306, 'user': 'tornado_user', 'password': 'ciel2019'})
# database.set_allow_sync(False)
# tornado 运行初始化端口 指定端口 --port == xxx
define("port", default=9004, help="run on the given port", type=int)
settings = {'debug': True, 'template_path': 'templates', 'static_path': "static", "xsrf_cookies": False}
AsyncIOMainLoop().install()
app = web.Application(
    handlers=[
        (r"/wifi", SendDataToWifi),
        (r"/mqtt", GetMqttData),
        # (r"/api/users/", GetAllUserHandler),
        (r"/user", GetUserHandler),
        (r"/", IndexHandler),
        (r"/test", Test),
        (r"/OAuth2Home", OAuth2Home),
        (r"/token", AccessTokenURL),
        (r"/RevTmCommand", RevTmCommand),
        (r"/WebHook", WebHook),
    ],
    **settings
)
app.objects = peewee_async.Manager(database=database)
if __name__ == "__main__":
    # app.objects.allow_sync = False
    # app.objects
    options.parse_command_line()
    # 初始化所有设备状态为0
    q = (WifiDevice.update(
        {WifiDevice.is_alive: 0}).where(
        WifiDevice.is_alive == '1'))
    q.execute()

    server = TcpHandler()
    server.listen(23333)
    server.start()
    PeriodicCallback(functools.partial(heartbeat), callback_time=30000).start()  # start scheduler 每隔10s执行一次发送心跳包

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

