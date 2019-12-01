import base64
import json
import struct
from paho.mqtt.client import Client
import paho.mqtt.client as mqtt
from models.smartroom import LoraDevice
from datetime import datetime


class Mqtt(Client):
    """
    lora设备订阅，参考文档 https://blog.csdn.net/jiangjunjie_2005/article/details/96358863
    """

    def on_connect(self, client, userdata, flags, rc):
        # 初始化DATA
        # global DATA
        # DATA = 'None'
        client.subscribe("application/1/device/3634374710300059/rx")

    def on_message(self, client, userdata, msg):
        # global DATA
        DATA = json.loads(msg.payload)
        # print(DATA)
        if isinstance(DATA, dict):
            DATA = base64.b64decode(DATA['data'])

            # print(DATA)
            LoraDevice.get_or_create(device_number='3634374710300059', defaults={'data': DATA, 'date': datetime.now()})
            # q = (LoraDevice.update(
            #     {LoraDevice.data: temperature + humidity, LoraDevice.date: datetime.now(),
            #      LoraDevice.is_alive: 1}).where(
            #     LoraDevice.device_name == '3634374710300059'))
            # q.execute()


class Mqtt2(Client):
    def on_connect(self, client, userdata, flags, rc):
        # 初始化DATA2
        client.subscribe("application/1/device/36343747104a002e/rx")

    def on_message(self, client, userdata, msg):
        # global DATA2
        DATA = json.loads(msg.payload)
        if isinstance(DATA, dict):
            DATA = base64.b64decode(DATA['data']).hex().upper()
            LoraDevice.get_or_create(device_name='36343747104a002e', defaults={'data': DATA, 'date': datetime.now()})
            # print('36343747104a002e',DATA)


class Mqtt3(Client):
    def on_connect(self, client, userdata, flags, rc):
        # 初始化DATA2
        global DATA3
        DATA3 = 'None'
        client.subscribe("application/1/device/363437470E280056/rx")

    def on_message(self, client, userdata, msg):
        global DATA3
        DATA3 = json.loads(msg.payload)
        if isinstance(DATA3, dict):
            DATA3 = base64.b64decode(DATA3['data']).hex().upper()


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


# def save_mqtt_data():
#     """
#     保存lora设备数据
#     :return:
#     """
#     global DATA, DATA2, DATA3
#
#     if isinstance(DATA, bytes):
#         temperature = str(struct.unpack('!f', DATA[0:4])[0])[:5]
#         humidity = str(struct.unpack('!f', DATA[4:8])[0])[:5]
#         # print(DATA)
#         # if(LoraDevice.get_or_create(device_number='3634374710300059',
#         #                                                    defaults={'data': temperature+humidity})):
#         q = (LoraDevice.update(
#             {LoraDevice.data: temperature + humidity, LoraDevice.date: datetime.now(), LoraDevice.is_alive: 1}).where(
#             LoraDevice.device_name == '3634374710300059'))
#         q.execute()
#         # app.objects.create(LoraDevice, device_name='3634374710300059', data=DATA)
#         del DATA
#         # logging.info('mqtt59保存数据')
#         # logging.info('mqtt59数据为空')
#         # pass
#     if DATA2 != 'None':
#         if(LoraDevice.get_or_create(device_name='36343747104a002e', defaults={'data': '0'})):
#             q = (LoraDevice.update(
#                 {LoraDevice.data: DATA2, LoraDevice.date: datetime.now(),
#                  LoraDevice.is_alive: 1}).where(
#                 LoraDevice.device_name == '36343747104a002e'))
#             q.execute()
#             print('DATA2数据为{}'.format(DATA2))
#     # if isinstance(DATA3, str):
    #     print('DATA2数据为{}'.format(DATA3))

