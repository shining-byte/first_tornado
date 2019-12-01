from tornado.web import RequestHandler, HTTPError
from models.smartroom import User
from service.lora_mqtt import send_mqtt
from handlers.base import BaseHandler
from models.smartroom import LoraDevice


class LoraIndexHandler(BaseHandler):
    """
    初始页面
    """

    async def get(self):
        # obj = await self.application.objects.create_or_get(LoraDevice, device_name='3634374710300059')
        # #             temperature = str(struct.unpack('!f', DATA[0:4])[0])[:5]
        # #             humidity = str(struct.unpack('!f', DATA[4:8])[0])[:5]
        # obj2 = await self.application.objects.create_or_get(LoraDevice, device_name='36343747104a002e')
        devices = LoraDevice.select()
        # print(obj2[0].data)
        await self.render("lora_devices.html",
                          # temperature=obj[0].data[0:5],
                          # date2=obj2[0].date, humidity=obj[0].data[5:10], date=obj[0].date,
                          devices=devices,
                          # temperature2=int(obj2[0].data[:4], 16)/10, humidity2=int(obj2[0].data[5:], 16)/10
                          )


class GetAllUserHandler(RequestHandler):
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


class GetUserHandler(RequestHandler):
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
            raise HTTPError(404, "objects not found, error:{}".format(e))


class GetMqttData(RequestHandler):
    """
    lora设备下发指令
    """

    def post(self):
        send_data = self.get_argument('send_data')
        status = send_mqtt(send_data)
        if status:
            self.set_status(200)
