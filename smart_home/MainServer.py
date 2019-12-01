from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.web import HTTPServer
from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.ioloop import IOLoop, PeriodicCallback
from service.timecontrol import TimeService
from peewee_async import Manager
from handlers import login, course, schedule, tmall, mqtt, index,control_device
from service.device_connection import TcpHandler, heartbeat
from service.lora_mqtt import Mqtt, Mqtt2
from models.smartroom import WifiDevice
import functools
import config


route=[
    (r'/login', login.LoginHandler),
    (r'/logout', login.LogoutHandler),
    (r'/getDevices',control_device.getDevices),
    (r'/controlDevice',control_device.controlDevice),
    (r'/quickSwitcher',control_device.quickSwitcher),
    (r'/index', index.TestIndexHandler),
    (r"/test", index.TestHandler),
    (r'/', index.IndexHandler),
    (r"/mqtt", mqtt.GetMqttData),
    (r"/lora", mqtt.LoraIndexHandler),
    (r'/setCourse',course.SetCourseHandler),
    (r'/getCourse',course.GetCourseHandler),
    (r'/getClassRoom', course.GetRoomHandler),
    (r'/bookRoom', schedule.BookRoomHandler),
    (r'/modifySchedule', schedule.ModifyScheduleHandler),
    (r"/OAuth2Home", tmall.OAuth2Home),
    (r"/token", tmall.AccessTokenURL),
    (r"/RevTmCommand", tmall.RevTmCommand),
    (r"/WebHook", tmall.WebHook),
    (r"/wifi", index.SendDataToWifi),
    (r'/(.*)$', StaticFileHandler, {
        "path": config.setting["static_path"]
    })
]

if __name__=="__main__":
    AsyncIOMainLoop().install()
    objects = Manager(config.database)
    # 开启时间服务,须在app前开启
    timeservice = TimeService()
    # config.database.set_allow_sync(False)

    # 初始化所有设备状态为0
    q = (WifiDevice.update(
        {WifiDevice.is_alive: 0}).where(
        WifiDevice.is_alive == '1'))
    q.execute()

    server = TcpHandler()
    server.listen(23333)
    server.start()
    PeriodicCallback(functools.partial(heartbeat), callback_time=30000).start()  # start scheduler 每隔30s执行一次发送心跳包

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

    # PeriodicCallback(functools.partial(save_mqtt_data), callback_time=5000).start()

    app=Application(route,**config.setting)
    app.objects = objects
    server=HTTPServer(app)
    server.listen(config.port)
    IOLoop.current().start()



