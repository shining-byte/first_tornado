from tornado.web import MissingArgumentError

from handlers.base import BaseHandler
from models.smartroom import WifiDevice,ClassRoom
from service.device_control import DeviceController,DeviceNotExistException
from config import code,logging

class getDevices(BaseHandler):
    async def get(self):
        try:
            room=self.get_query_argument("room")
            await self.application.objects.get(ClassRoom,name=room)
            devices=await self.application.objects.execute(WifiDevice.select().where(WifiDevice.class_number==room))
            devices_list=[]
            for device in devices:
                device_dic={}
                device_dic["device_name"] = device.device_number
                if device.device_number=="0":
                    device_dic["device_name"] = device.device_name
                    device_dic["degree"] = device.degree
                device_dic["status"]=device.status
                device_dic["is_alive"]=device.is_alive
                devices_list.append(device_dic)
            self.write({
                "code": code["success"],
                "devices": devices_list
            })
        except ClassRoom.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该教室"
            })
        except MissingArgumentError:
            self.write({
                "code": code["fail"],
                "msg": "缺少参数"
             })

class controlDevice(BaseHandler):
    async def post(self):
        try:
            room=self.get_body_argument("room")
            device_name=self.get_body_argument("device_name")
            status=int (self.get_body_argument("status"))
            degree =self.get_body_argument("degree", default=None)
            await self.application.objects.get(ClassRoom, name=room)

            device = await self.application.objects.get(WifiDevice, device_number=device_name, class_number=room)
            contorller = DeviceController(device.device_name, device.class_number)
            if "air" in device_name:
                if status == 0:
                    contorller.turn_off_air()
                else:
                    contorller.turn_on_air()
                    if degree:
                        int(degree)
                        controller.setDegree(degree)
            else :
                if status == 0:
                    contorller.turn_off(device.device_number)
                else:
                    contorller.turn_on(device.device_number)

            await contorller.send()
            self.write({
                "code": code["success"]
            })
        except ClassRoom.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该教室"
            })
        except DeviceNotExistException:
            self.write({
                "code": code["fail"],
                "msg": "设备不在线"
            })
        except WifiDevice.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该设备"
            })
        except MissingArgumentError:
            self.write({
                "code": code["fail"],
                "msg": "缺少参数"
            })
        except ValueError:
            self.write({
                "code": code["fail"],
                "msg": "数值参数错误"
            })


class quickSwitcher(BaseHandler):
    async def post(self):
        try:
            room = self.get_body_argument("room")
            status = int(self.get_body_argument("status"))
            await self.application.objects.get(ClassRoom, name=room)
            airs = await self.application.objects.execute(WifiDevice.select().where((WifiDevice.device_name % 'air%') & (WifiDevice.class_number==room)))
            devices = await self.application.objects.execute(WifiDevice.select().where((WifiDevice.device_name % 'fan%') & (WifiDevice.class_number==room)))
            dead_devices=[]

            for air in airs:
                if air.is_alive:
                    # 创建控制器执行命令,空调在单独的板，需要单独设置
                    air_contorller = DeviceController(air.device_name, air.class_number)
                    if status:
                        air_contorller.turn_on_air()
                    else:
                        air_contorller.turn_off_air()
                    await air_contorller.send()
                else :
                    dead_devices.append(air.device_number)

            # 控制风扇，灯，窗帘
            contorller = DeviceController(devices[0].device_name, devices[0].class_number)
            for device in devices:
                if device.is_alive:
                    if status:
                        contorller.turn_on(device.device_number)
                    else:
                        contorller.turn_off(device.device_number)
                else:
                    dead_devices.append(device.device_number)
            await contorller.send()

            self.write({
                "code": code["success"],
                "DeadDevices":dead_devices
            })
        except DeviceNotConnectException:
            self.write({
                "code": code["fail"],
                "msg": "控制板掉线，请稍候再试"
            })
        except DeviceNotExistException:
            self.write({
                "code": code["fail"],
                "msg": "设备全掉线"
            })
        except ClassRoom.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该教室"
            })
        except MissingArgumentError:
            self.write({
                "code": code["fail"],
                "msg": "缺少参数"
            })
        except ValueError:
            self.write({
                "code": code["fail"],
                "msg": "status参数错误"
            })

