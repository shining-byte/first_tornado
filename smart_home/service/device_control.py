import re

from service.device_connection import TCP_CONNECTION
from models.smartroom import WifiDevice, ClassRoom
from config import logging

class DeviceNotExistException(Exception):
    pass

class DeviceNotConnectException(Exception):
    pass

class DeviceController:
    def __init__(self, device_name, class_room):
        if not device_name + class_room in TCP_CONNECTION.keys():
            logging.info(TCP_CONNECTION.keys())
            raise DeviceNotConnectException

        result = WifiDevice.select() \
            .where(WifiDevice.class_number == class_room).execute()
        self.devices = []
        for device in result:
            self.devices.append(device.device_number)
        self.device_name = device_name
        self.class_room = class_room
        self.send_data = {"device_name": device_name, "class": class_room}

    def turn_on(self, *devices):
        self.__isExistDevice(*devices)
        for device in devices:
            self.send_data[device] = "1"

    def turn_off(self, *devices):
        self.__isExistDevice(*devices)
        for device in devices:
            self.send_data[device] = "0"
            
    async def turn_lamp_on(self, devices):
        self.__isExistDevice(*devices)
        for device in devices:
            if re.findall('lamp', device):
                self.send_data[device] = "1"
        await self.send()

    async def turn_lamp_off(self, devices):
        self.__isExistDevice(*devices)
        for device in devices:
            if re.findall('lamp', device):
                self.send_data[device] = "0"
        await self.send()

    async def turn_fan_on(self, devices):
        self.__isExistDevice(*devices)
        for device in devices:
            if re.findall('fan', device):
                self.send_data[device] = "1"
        await self.send()

    async def turn_curtain_on(self, devices):
        self.__isExistDevice(*devices)
        for device in devices:
            if re.findall('curtain', device):
                self.send_data[device] = "1"
        await self.send()

    async def turn_curtain_off(self, devices):
        self.__isExistDevice(*devices)
        for device in devices:
            if re.findall('curtain', device):
                self.send_data[device] = "0"
        await self.send()

    async def turn_fan_off(self, devices):
        self.__isExistDevice(*devices)
        for device in devices:
            if re.findall('fan', device):
                self.send_data[device] = "0"
        await self.send()

    async def turn_devices_off(self, devices):
        self.__isExistDevice(*devices)
        for device in devices:
            if re.findall('air', device):
                pass
            else:
                self.send_data[device] = "0"
        await self.send()

    async def turn_devices_on(self, devices):
        self.__isExistDevice(*devices)
        for device in devices:
            if re.findall('air', device):
                pass
            else:
                self.send_data[device] = "1"
        await self.send()

    def turn_on_air(self):
        self.send_data['status']='1'
        self.send_data["degree"]='25'
        self.send_data['gear']='5'
        self.send_data['model']='1'

    def turn_off_air(self):
        self.send_data['status'] = '0'

    async def turn_air_on(self):
        self.send_data['status'] = '1'
        self.send_data["degree"] = '25'
        self.send_data['gear'] = '5'
        self.send_data['model'] = '1'
        await self.send()

    async def turn_air_off(self):
        self.send_data['status'] = '0'
        await self.send()

    def stop(self, *devices):
        self.__isExistDevice(*devices)
        for device in devices:
            self.send_data[device] = "2"

    def setGear(self, **devices):
        self.__isExistDevice(devices.keys())
        for device, gear in devices.items():
            self.send_data[device] = gear

    def setDegree(self,degree):
        self.send_data["degree"]=degree

    def __isExistDevice(self, *devices):
        print('self.devices: {}'.format(self.devices))
        print(devices)
        for device in devices:
            if not device in self.devices:
                 raise DeviceNotExistException

    async def send(self):
        print('----------------------self.send_data-',self.send_data)
        # logging.info(self.send_data)
        await TCP_CONNECTION[self.device_name + self.class_room].write(
            bytes(str(self.send_data), encoding='utf-8'))

