import json
import re
from service.device_connection import TCP_CONNECTION
from handlers.base import BaseHandler
from models.smartroom import WifiDevice, LoraDevice
from config import database,logging
from service.device_control import DeviceController, DeviceNotExistException
class IndexHandler(BaseHandler):
    def get(self):
        self.teacher = self.get_session()["teacher"]
        if self.teacher:
            return self.render("index.html")
        else:
            return self.redirect("/smarthome/login.html")


class TestIndexHandler(BaseHandler):
    """
    初始页面
    """

    async def get(self):
        # obj = await self.application.objects.create_or_get(LoraDevice, device_name='3634374710300059')
        # #             temperature = str(struct.unpack('!f', DATA[0:4])[0])[:5]
        # #             humidity = str(struct.unpack('!f', DATA[4:8])[0])[:5]
        # obj2 = await self.application.objects.create_or_get(LoraDevice, device_name='36343747104a002e')
        devices = WifiDevice.select()
        # print(obj2[0].data)
        await self.render("indextest.html",
                          # temperature=obj[0].data[0:5],
                          # date2=obj2[0].date, humidity=obj[0].data[5:10], date=obj[0].date,
                          devices=devices,
                          # temperature2=int(obj2[0].data[:4], 16)/10, humidity2=int(obj2[0].data[5:], 16)/10
                          )

    # def prepare(self):
    #     database.connect()
    #     return super(IndexHandler, self).prepare()
    #
    # def on_finish(self):
    #     if not database.is_closed():
    #         database.close()
    #     return super(IndexHandler, self).on_finish()


class TestHandler(BaseHandler):
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
        on5 = self.get_arguments("on-7-lamp")
        off5 = self.get_arguments("off-7-lamp")
        on6 = self.get_arguments("on-7-fan")
        off6 = self.get_arguments("off-7-fan")
        off7 = self.get_arguments("off-7-air")
        on7 = self.get_arguments("on-7-air")
        on8 = self.get_arguments("on-10-air")
        off8 = self.get_arguments("off-10-air")

        on9 = self.get_arguments("on-all")
        on10 = self.get_arguments("on-09-air")
        on11 = self.get_arguments("on-09-lamp")
        on12 = self.get_arguments("on-09-curtain")

        off9 = self.get_arguments("off-all")
        off10 = self.get_arguments("off-09-air")
        off11 = self.get_arguments("off-09-lamp")
        off12 = self.get_arguments("off-09-curtain")
        if (offlamp):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'lamp-1': '0', 'lamp-2': '0','lamp-3': '0'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'fan-1': '0'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'curtain-1': '0'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'curtain-1': '2'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'curtain-1': '1'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'fan-2': '0'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'fan-3': '0'}'''
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
        elif (off5):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'D712', 'lamp-1': '0', 'lamp-2': '0'}'''
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
        elif (on7):
            send_data = '''{'device_name': 'air-1', 'class': 'D712', 'status' :'1' , 'gear': '5', 'degree': '25', 'model': '1'}'''
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
        elif (on8):
            send_data = '''{'device_name': 'air-1', 'class': 'C1004', 'status': '1', 'gear': '1', 'degree': '25', 'model': '1' }'''
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
        elif (off7):
            send_data = '''{'device_name': 'air-1', 'class': 'D712', 'status': '0' }'''
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
        elif (off8):
            send_data = '''{'device_name': 'air-1', 'class': 'C1004', 'status': '0' }'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'lamp-1': '1', 'lamp-2': '1','lamp-3': '1'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'fan-1': '2'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'fan-2': '2'}'''
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
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'fan-3': '2'}'''
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
        elif (on5):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'D712', 'lamp-1': '1', 'lamp-2': '1'}'''
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
        elif (on6):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'D712', 'fan-1': '1', 'fan-2': '1', 'fan-3': '1', 'fan-4': '1'}'''
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
        elif (off6):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'D712', 'fan-1': '0', 'fan-2': '0', 'fan-3': '0', 'fan-4': '0'}'''
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
                

        elif (on9):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'D910'}'''
            # try:
            send_data = eval(send_data)
            if isinstance(send_data, dict):
                # if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                devices = WifiDevice.select() \
                    .where(WifiDevice.class_number == send_data['class']).execute()
                list_ = [device.device_number for device in devices]
                    # await device_controller.turn_devices_on(list_)
                for j in list_:
                    if re.findall('air', j):
                        await DeviceController(j, send_data['class']).turn_air_on()
                    else:
                # for k in other_list:
                        await DeviceController(j[0:-2], send_data['class']).turn_devices_on(list_)
                return_data = {'status': 200, 'message': 'success'}
                self.write(json.dumps(return_data))
                # else:
                #     return_data = {'status': 500, 'message': 'failure, 设备TCP未连接'}
                #     self.write(json.dumps(return_data))
            else:
                return_data = {'status': 500, 'message': 'failure, 命令有误'}
                self.write(json.dumps(return_data))
            # except Exception as e:
            #     return_data = {'status': 500, 'message': 'failure, track:{}'.format(e)}
                #
                # del TCP_CONNECTION[send_data['device_name']]
                # self.write(json.dumps(return_data))
                
        elif (on10):
            send_data = '''{'device_name': 'air-1', 'class': 'D910',  'status': '1', 'gear': '1', 'degree': '25', 'model': '1'}'''
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
                
        elif (on11):
            send_data = '''{'device_name': 'lamp', 'class': 'D910', 'lamp-1': '1'}'''
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
                
        elif (on12):
            send_data = '''{'device_name': 'curtain', 'class': 'D910', 'curtain-1': '1'}'''
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
        elif (off9):
            send_data = '''{'device_name': 'fan-lamp-curtain', 'class': 'D910'}'''
            # try:
            send_data = eval(send_data)
            if isinstance(send_data, dict):
                # if send_data['device_name'] + send_data['class'] in TCP_CONNECTION.keys():
                devices = WifiDevice.select() \
                    .where(WifiDevice.class_number == send_data['class']).execute()
                list_ = [device.device_number for device in devices]
                    # await device_controller.turn_devices_on(list_)
                for j in list_:
                    if re.findall('air', j):
                        await DeviceController(j, send_data['class']).turn_air_off()
                    else:
                # for k in other_list:
                        await DeviceController(j[0:-2], send_data['class']).turn_devices_off(list_)
                return_data = {'status': 200, 'message': 'success'}
                self.write(json.dumps(return_data))
                #
                # del TCP_CONNECTION[send_data['device_name']]
                self.write(json.dumps(return_data))
        elif (off10):
            send_data = '''{'device_name': 'air-1', 'class': 'D910', 'status': '0'}'''
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
        elif (off11):
            send_data = '''{'device_name': 'lamp', 'class': 'D910', 'lamp-1': '0'}'''
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
        elif (off12):
            send_data = '''{'device_name': 'curtain', 'class': 'D910', 'curtain-1': '0'}'''
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


class SendDataToWifi(BaseHandler):
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