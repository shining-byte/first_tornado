from handlers.base import BaseHandler
from config import logging
from Tmall.TmallDeivces import D712_devices, D910_devices, C1004_devices
from service.device_connection import TCP_CONNECTION
from service.device_control import DeviceController, DeviceNotExistException
from models.smartroom import WifiDevice
from tornado import auth
import random
import string
import re
import time


class OAuth2Home(BaseHandler, auth.OAuth2Mixin):
    """
    天猫精灵获取授权
    """

    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    _OAUTH_AUTHORIZE_URL = 'https://ciel.pub/OAuth2Home'

    # https://xxx.com/auth/authorize?redirect_uri=https%3A%2F%2Fopen.bot.tmall.com%2Foauth%2Fcallback%3FskillId%3D11111111%26token%3DXXXXXXXXXX&client_id=XXXXXXXXX&response_type=code&state=111
    # 验证天猫上精灵填写的client_id,
    async def get(self):
        if self.get_arguments('code'):
            # self.write({'code': self.get_argument('code'), 'url':self.get_argument('redirect_uri')})
            url = self.get_argument('redirect_uri') + "&code=" + self.get_argument(
                'code') + "&state=" + self.get_argument('state')
            self.redirect(url=url)
        else:
            client_id = self.get_arguments('client_id')[0]
            print(client_id,'---------------------------------')
            # if client_id == 'D712':
                # code = ''.join(random.sample(string.ascii_letters + string.digits, 40))+
                # code = 'D712'
            self.authorize_redirect(
                redirect_uri=self.get_argument('redirect_uri'),
                client_id=self.get_argument('client_id'),
                # scope=['profile', 'email'],
                response_type=self.get_argument('response_type'),
                extra_params={'state': self.get_argument('state'), 'code': client_id},
            # extra_params={'approval_prompt': 'auto'}
            )


class AccessTokenURL(BaseHandler):
    """
    天猫精灵获取access token
    """

    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    async def post(self):
        grant_type = self.get_argument('grant_type')

        if grant_type == 'refresh_token':
            # https://XXXXX/token?grant_type=refresh_token&client_id=XXXXX&client_secret=XXXXXX&refresh_token=XXXXXX
            logging.info('refresh_token')
            client_id = self.get_arguments('client_id')
            # 验证refresh_token
            # access_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            access_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            refresh_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            # refresh_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
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
            #     access_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            access_token = code
            # refresh_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            refresh_token = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": 3600,
            }
            self.write(data)

class RevTmCommand(BaseHandler):
    """
    天猫精灵post指令网关
    """

    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    async def post(self):
        dicts = eval(self.request.body.decode('utf-8'))
        print(dicts)
        if dicts['header']['namespace'] == "AliGenie.Iot.Device.Discovery":
            if dicts['payload']['accessToken'] == 'D712':
            # from TmallDevices import devices
                self.write(D712_devices)
            elif dicts['payload']['accessToken'] == 'D910':
                self.write(D910_devices)
            elif dicts['payload']['accessToken'] == 'C1004':
                self.write(C1004_devices)
        elif dicts['header']['namespace'] == "AliGenie.Iot.Device.Control":
            name = dicts['header']['name']
            messageId = dicts['header']['messageId']
            deviceType = dicts['payload']['deviceType']
            deviceId = dicts['payload']['deviceId']
            class_number = dicts['payload']['accessToken']
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
            device_name = deviceId[0:-1]
            devices = WifiDevice.select() \
                .where((WifiDevice.class_number == class_number) & (WifiDevice.device_name == device_name)).execute()
            # print()
            device_controller = DeviceController(device_name, class_number)
            if deviceType in ['fan', 'curtain', 'light']:
                device_list = [device.device_number for device in devices]
                print(device_list)
                if name == 'TurnOn':
                    for _ in range(2):
                        print('开')
                        if deviceType == 'fan':
                            await device_controller.turn_fan_on(device_list)
                        elif deviceType == 'light':
                            await device_controller.turn_lamp_on(device_list)
                        elif deviceType == 'curtain':
                            await device_controller.turn_curtain_on(device_list)
                        time.sleep(0.2)
                elif name == 'TurnOff':
                    if deviceType == 'fan':
                        print('关')
                        await device_controller.turn_fan_off(device_list)
                    elif deviceType == 'light':
                        await device_controller.turn_lamp_off(device_list)
                    elif deviceType == 'curtain':
                        await device_controller.turn_curtain_off(device_list)
                    return_data['header']['name'] = 'TurnOffResponse'
            elif deviceType == 'aircondition':
                if name == 'TurnOn':
                    # for _ in range(2):
                    device_controller.turn_on_air()
                    await device_controller.send()
                        # time.sleep(0.2)
                elif name == 'TurnOff':
                    device_controller.turn_off_air()
                    await device_controller.send()
                    return_data['header']['name'] = 'TurnOffResponse'
                elif name == 'SetTemperature':
                    device_controller.setDegree(str(dicts['payload']['value']))
                    await device_controller.send()
                    return_data['header']['name'] = 'SetTemperatureResponse'
                elif name == 'AdjustUpTemperature':
                    # degree = WifiDevice.select
                    # print(devices[0].degree)
                    # print(type(devices[0].degree))
                    # print(devices.degree)
                    device_controller.setDegree(str(int(devices[0].degree)+1))
                    await device_controller.send()
                    return_data['header']['name'] = 'AdjustUpTemperatureResponse'
                elif name == 'AdjustDownTemperature':
                    # degree = WifiDevice.select
                    # print(devices[0].degree)
                    # print(type(devices[0].degree))
                    # print(devices.degree)
                    device_controller.setDegree(str(int(devices[0].degree)-1))
                    await device_controller.send()
                    return_data['header']['name'] = 'AdjustDownTemperatureResponse'
            self.write(return_data)


class WebHook(BaseHandler):
    """
    天猫技能接口
    """

    def set_default_header(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

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
        get_json = get_json.replace('true', '1')
        dicts = eval(get_json.replace('false', '0'))
        # print(/)
        # 这里由天猫精灵开发者平台定义请求头
        # headers = str(self.request.headers).lower()
        # headers = eval(headers)

        # command['action'] = self.request.headers['action']
        class_number = self.request.headers['class']
        try:
            if dicts['skillName'] == '全部设备':
                devices_ = self.request.headers['devices']
                devices_list = devices_.split('+')
                print(devices_)
                devices = WifiDevice.select() \
                    .where(WifiDevice.class_number == class_number).execute()
                air_list = []
                other_list = []
                for j in devices_list:
                    if re.findall('air', j):
                        air_list.append(j)
                    else:
                        other_list.append(j)
                # device_controller = [DeviceController(k, class_number) for k in other_list]
                list_ = [device.device_number for device in devices]
                if self.request.headers['action'] == 'on':
                    print('action ==1 ')
                    # await device_controller.turn_devices_on(list_)
                    for j in air_list:
                        await DeviceController(j, class_number).turn_air_on()
                        time.sleep(0.3)
                    for k in other_list:
                        await DeviceController(k, class_number).turn_devices_on(list_)
                        # time.sleep(0.3)
                    # device_controller_air.turn_on_air()
                    # await device_controller_air.send()
                    return_dict['returnValue']['reply'] = "好的，又是元气满满的一天哦。"
                    self.write(return_dict)
                elif self.request.headers['action'] == 'off':
                    print('action ==0')
                    for k in other_list:
                        await DeviceController(k, class_number).turn_devices_off(list_)
                        time.sleep(1)
                    for j in air_list:
                        await DeviceController(j, class_number).turn_air_off()
                        time.sleep(1)
                    # device_controller_air.turn_off_air()
                    # await device_controller_air.send()
                    return_dict['returnValue']['reply'] = "好的，祝您晚上有个好梦哦。"
                    self.write(return_dict)
            elif dicts['skillName'] == '领导来了':
                return_dict['returnValue']['actions'][0]['properties']['audioGenieId'] = "24976"
                return_dict['returnValue']['reply'] = '。'
                self.write(return_dict)
                # time.sleep(1)
                if ('lamp' + class_number in TCP_CONNECTION.keys()) and ('curtain' + class_number in TCP_CONNECTION.keys()):
                    await TCP_CONNECTION['lamp' + class_number].write(
                        bytes(str('''{'device_name': 'lamp', 'class': 'D910', 'lamp-1': '1'}'''), encoding='utf-8'))
                    await TCP_CONNECTION['curtain' + class_number].write(
                        bytes(str('''{'device_name': 'curtain', 'class': 'D910', 'curtain-1': '1'}'''), encoding='utf-8'))

                else:
                    return_dict['returnValue']['reply'] = "设备未连接"
                    self.write(return_dict)
            else:
                return_dict['returnValue']['reply'] = "未识别意图"
                # logging.info('非{}'.format(return_dict))
                self.write(return_dict)
        except Exception as e:
            print('出错了{}'.format(e))
            self.write(return_dict)

