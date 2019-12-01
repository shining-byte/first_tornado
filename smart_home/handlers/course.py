# Date='2019/9/30 20:07'
# File Name='course'
# AUTHOR='Tony'
import json

from tornado.web import authenticated
from config import code
from handlers.base import BaseHandler
from models.smartroom import *
from service.timecontrol import TimeService
from service.timecontrol import SessionError

service = TimeService()
class SetCourseHandler(BaseHandler):


    def prepare(self):
        # 检验json数据,非json就返回失败
        if self.request.body:
            try:
                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                self.write({
                    "code": code["fail"],
                    "msg": "json格式错误"
                })
                self.finish()
        return super(SetCourseHandler, self).prepare()
    # 问题：暂没session数值限制
    # 修改课表
    @authenticated
    async def post(self):
        try:
            data=json.loads(self.request.body.decode('utf-8'))
            course=data["course"]

            # 开启事务，异常便自动回滚
            async with self.application.objects.atomic():
                for single_course in course:
                    date=single_course.get("date")
                    name=single_course.get("name")
                    class_name=single_course.get("class")
                    session=single_course.get("session")
                    where=single_course.get("where")
                    service.checkFormat(date, session)
                    # 找出需要修改的课表,没有则设置为空
                    try:
                        update_course = await self.application.objects.get(Course, date=date, session=session,
                                                                        teacher_id=self.teacher.id)
                    except Course.DoesNotExist:
                        update_course=None

                    #不存在就创建一个课表，存在就修改
                    if update_course:
                        update_course.name=name
                        update_course.class_name=class_name

                        # 有where参数则用where,没有则用本来的where
                        if where:
                            room_id = (await self.application.objects.get(ClassRoom, name=where)).id
                        else:
                            room_id = update_course.room_id

                        update_course.room_id=room_id
                        await self.application.objects.update(update_course)
                    else:
                        room_id = (await self.application.objects.get(ClassRoom, name=where)).id
                        temple_course = {
                            "room_id": room_id,
                            "teacher_id": self.teacher.id,
                            "date":date,
                            "name": name,
                            "class_name": class_name,
                            "session": session
                        }
                        await self.application.objects.create(Course, **temple_course)

            self.write({
                "code": code["success"]
            })

        except KeyError:
            self.write({
                "code": code["fail"],
                "msg": "缺少参数"
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
        except ValueError:
            self.write({
                "code": code["fail"],
                "msg": "日期格式错误"
            })

class GetCourseHandler(BaseHandler):
    # 获取课表
    @authenticated
    async def get(self):
        try:
            # 没有参数则为空
            post_date=self.get_query_argument("date",default=None)
            # 如果不存在参数date就获取当天的日期
            if not post_date:
                post_date=service.date
            # 格式不对则抛出异常
            weekday=int(service.getWeekDay(post_date))
            list_date=service.getSeqWeek(post_date)
            # 构造返回数据
            one_week_course=[]
            for date in list_date:
                one_day_course={}
                one_day_course["date"]=date
                # 获取课表按照上课顺序排序
                courses=await self.application.objects.execute(Course.select().where((Course.date==date) & (Course.teacher_id==self.teacher.id)).order_by(Course.session))
                temp_course_list=[]

                for course in courses:
                    where=await self.application.objects.get(ClassRoom,id=course.room_id)
                    temp_course_list.append({
                        "name":course.name,
                        "class":course.class_name,
                        "session":course.session,
                        "where":where.name
                    })
                one_day_course["course"]=temp_course_list
                one_week_course.append(one_day_course)
            respon={
                "code":code["success"],
                "thatday":post_date,
                "weekday":weekday,
                "one_week_course":one_week_course
            }
            self.write(respon)
        except ValueError:
            self.write({
                "code": code["fail"],
                "msg": "日期错误"
            })


class GetRoomHandler(BaseHandler):
    @authenticated
    async def get(self):
        try:
            rooms = await self.application.objects.execute(ClassRoom.select())
            temp_room_list=[]
            for room in rooms:
                temp_room_list.append(room.name)

            self.write({
                "code":code["success"],
                "rooms":temp_room_list
            })
        except ClassRoom.DoesNotExist:
            self.write({
                "code": code["fail"],
                "msg": "不存在该教室"
            })
