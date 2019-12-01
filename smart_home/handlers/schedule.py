from tornado.web import MissingArgumentError
from service.timecontrol import TimeService, SessionError
from tornado.web import authenticated
from handlers.base import BaseHandler
from models.smartroom import *
from config import code, session_time
import time

service = TimeService()


# 太晚预订错误
class LateScheduleException(Exception):
    pass


# 预约开始前一分钟内禁止修改
def checkScheduleTime(date, session):
    session = int(session)
    if service.date == date:
        hour = session_time["start"][session][0]
        min = session_time["start"][session][1]
        nhour = int(time.strftime("%H", time.localtime()))
        nmin = int(time.strftime("%M", time.localtime())) + 1
        if hour == nhour and min == nmin:
            raise LateScheduleException


class BookRoomHandler(BaseHandler):
    @authenticated
    async def post(self):
        try:
            date = self.get_body_argument("date")
            where = self.get_body_argument("where")
            session = self.get_body_argument("session")
            service.checkFormat(date, session)
            checkScheduleTime(date, session)
            room = await self.application.objects.get(ClassRoom, name=where)
            # 判断是否存在课表
            await self.application.objects.get(Course, date=date, room_id=room.id, session=session)
            try:
                table = await self.application.objects.get(Scheduler_Table, date=date, room_id=room.id, session=session)
            except Scheduler_Table.DoesNotExist:
                table = None
            # 判断是否冲突课表,以及是否预约其他课室,保证同一时间只能预约一间课室
            if not table:
                try:
                    await self.application.objects.get(Scheduler_Table, date=date, teacher_id=self.teacher.id,
                                                       session=session)
                    self.write({
                        "code": code["fail"],
                        "msg": "已预约了其他教室"
                    })
                    self.finish()
                    return
                except Scheduler_Table.DoesNotExist:
                    await self.application.objects.create(Scheduler_Table, room_id=room.id, date=date,
                                                          teacher_id=self.teacher.id,
                                                          session=session)
                    self.write({
                        "code": code["success"]
                    })
                    self.finish()
                    return

            elif self.teacher.id != table.teacher_id:
                # 预约有冲突
                teacher = await self.application.objects.get(Teacher, id=table.teacher_id)
                self.write({
                    "code": code["fail"],
                    "msg": teacher.name + "已预约了该课室"
                })
                self.finish()
                return
            self.write({
                "code": code["fail"],
                "msg": "已预约了该课室"
            })
        except MissingArgumentError:
            self.write({
                "code": code["fail"],
                "msg": "缺少参数"
            })
        except Course.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该课表"
            })

        except ClassRoom.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该教室"
            })
        except SessionError:
            self.write({
                "code": code["fail"],
                "msg": "节数格式错误"
            })
        except LateScheduleException:
            self.write({
                "code": code["fail"],
                "msg": "预约前一分钟禁止修改"
            })
        except ValueError:
            self.write({
                "code": code["fail"],
                "msg": "日期格式错误"
            })


class GetSheduleHandler(BaseHandler):
    @authenticated
    async def get(self):
        try:
            date = self.get_query_argument("date", default=None)
            if not date:
                date = service.date
            week = service.getSeqWeek(date)
            schedule = []
            for day in week:
                result = self.application.object.execute(Scheduler_Table.select().where(
                    (Scheduler_Table.date == day) & (Scheduler_Table.teacher_id == self.teacher.id)).order_by(
                    Scheduler_Table.session))
                session = []
                schedule_date = {}
                for item in result:
                    session.append(item.session)
                schedule_date["date"] = day
                schedule_date["session"] = session
                schedule.append(schedule_date)

            self.write({
                "code": 1,
                "schedule": schedule
            })


        except ValueError:
            self.write({
                "code": code["fail"],
                "msg": "日期格式错误"
            })

class ModifyScheduleHandler(BaseHandler):
    @authenticated
    async def post(self):
        try:
            date = self.get_body_argument("date")
            where = self.get_body_argument("where")
            session = self.get_body_argument("session")
            service.checkFormat(date, session)
            checkScheduleTime(date, session)
            room = await self.application.objects.get(ClassRoom, name=where)
            table = await self.application.objects.get(Scheduler_Table, date=date, session=session,
                                                       teacher_id=self.teacher.id)
            table.room_id = room.id
            await self.application.objects.update(table)
            self.write({
                "code": code["success"],
            })
        except Scheduler_Table.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该预约"
            })
        except ClassRoom.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该房间"
            })
        except SessionError:
            self.write({
                "code": code["fail"],
                "msg": "节数格式错误"
            })
        except LateScheduleException:
            self.write({
                "code": code["fail"],
                "msg": "预约前一分钟禁止修改"
            })
        except MissingArgumentError:
            self.write({
                "code": code["fail"],
                "msg": "缺少参数"
            })
        except ValueError:
            self.write({
                "code": code["fail"],
                "msg": "日期格式错误"
            })
