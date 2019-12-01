# 时间控制器

import time,datetime
from apscheduler.schedulers.tornado import TornadoScheduler

from service.singlemode import Singleton
from models.smartroom import Scheduler_Table,WifiDevice,ClassRoom
from service.device_control import DeviceController
from config import session_time
from config import logging
#预约可能遇到的几种问题:
# 上课时间与下课时间相隔太短，应提前多少分钟开启电器
#上课时间中不能取消预约，需在页面中关闭课室的电器


#处理预约机制
#每天上课前10分钟提取数据库预约信息

class SessionError(ValueError):
    pass

@Singleton
class TimeService:
    def __init__(self):
        # 获取今天的时间和星期数
        self.date=time.strftime("%Y-%m-%d",time.localtime())
        self.weekday=time.strftime("%w",time.localtime())
        # 每天刷新
        scheduler=TornadoScheduler()
        scheduler.add_job(self._daytask,'cron',hour='0')

        scheduler.add_job(self.session_start,'cron',(1,),hour=session_time["start"][1][0],minute=session_time["start"][1][1])
        scheduler.add_job(self.session_start,'cron',(3,),hour=session_time["start"][3][0],minute=session_time["start"][3][1])
        scheduler.add_job(self.session_start,'cron',(5,),hour=session_time["start"][5][0],minute=session_time["start"][5][1])
        scheduler.add_job(self.session_start,'cron',(7,),hour=session_time["start"][7][0],minute=session_time["start"][7][1])
        scheduler.add_job(self.session_start,'cron',(9,),hour=session_time["start"][9][0],minute=session_time["start"][9][1])
        scheduler.start()


    # 每天刷新时间
    def _daytask(self):
        self.date = time.strftime("%Y-%m-%d", time.localtime())
        self.weekday = time.strftime("%w", time.localtime())

    # 获取日期的星期数
    def getWeekDay(self,date):
        return time.strftime("%w",time.strptime(date,"%Y-%m-%d"))


    # 给定一个日期，获取该日期一周的日期
    def getSeqWeek(self,date):
        weekday=int(self.getWeekDay(date))

        # 格式化日期为datetime进行加减
        cur_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        mon=cur_date-datetime.timedelta(days=weekday)
        list_date=[]
        for i in range(7):
            list_date.append((mon+datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        return list_date

    # 检验时间
    def checkFormat(self, date, session):
        time.strptime(date, "%Y-%m-%d")
        if not session in ['1', '3', '5', '7', '9']:
            raise SessionError

    # 上课开始的任务
    async def session_start(self,session):
        sc_tables=Scheduler_Table.select().where((Scheduler_Table.date==self.date) & (Scheduler_Table.session==session)).execute()
        # 上课做的事
        for sc_table in sc_tables:
            room = ClassRoom.get(id=sc_table.room_id)
            airs = WifiDevice.select().where((WifiDevice.device_name % 'air%') & (WifiDevice.class_number==room.name)).execute()
            devices = WifiDevice.select().where((WifiDevice.device_name % 'fan%') & (WifiDevice.class_number==room.name)).execute()
            for air in airs:
                # 创建控制器执行命令,空调在单独的板，需要单独设置
                air_contorller = DeviceController(air.device_name, air.class_number)
                air_contorller.turn_on_air()
                await air_contorller.send()

            # 控制风扇，灯，窗帘
            contorller = DeviceController(devices[0].device_name, devices[0].class_number)
            for device in devices:
                contorller.turn_on(device.device_number)
            await contorller.send()

            # 开始下课任务
            end_session_schedule=TornadoScheduler()
            end_session_schedule.add_job(self.session_end,'cron',(end_session_schedule,airs,devices,session,),hour=session_time["end"][session][0],minute=session_time["end"][session][1])
            end_session_schedule.start()
            logging.info("room_id: "+str(sc_table.room_id)+" open date: "+self.date+" session: "+str(session))


    # 下课结束的任务
    async def session_end(self,end_session_schedule,airs,devices,session):
        #下课做的事
        for air in airs:
            # 创建控制器执行命令,空调在单独的板，需要单独设置
            air_contorller = DeviceController(air.device_name, air.class_number)
            air_contorller.turn_off_air()
            await air_contorller.send()

        # 控制风扇，灯，窗帘
        contorller = DeviceController(devices[0].device_name, devices[0].class_number)
        for device in devices:
            contorller.turn_off(device.device_number)
        await contorller.send()

        logging.info("room_id: " + str(room_id) + " end date: " + self.date + " session: " + str(session))
        try:
            # 强行关闭该定时器
            end_session_schedule.shutdown()
        except RuntimeError:
            return


