from peewee import *
from config import database
from datetime import datetime


class BaseModel(Model):
    class Meta:
        database=database


class Teacher(BaseModel):
    # name老师名字
    # account老师账户
    # passwd账号密码
    name=CharField(max_length=50)
    account = CharField(unique=True, max_length=50)
    passwd=CharField(max_length=50)


class Course(BaseModel):

    # name课程名字
    # class_name班级名字
    # session上课节次
    # date课程日期
    # room_id课室id
    # teacher_id老师id
    name=CharField(max_length=50)
    class_name=CharField(max_length=50)
    session=IntegerField()
    room_id=IntegerField()
    date=DateField()
    teacher_id=IntegerField()


class ClassRoom(BaseModel):
    # name课室名字
    name=CharField(max_length=50)


class Scheduler_Table(BaseModel):
    date = DateField()
    teacher_id = IntegerField()
    session = IntegerField()
    room_id = IntegerField()


class User(BaseModel):
    username = CharField(unique=True, verbose_name='用户名', max_length=50)
    password = CharField(null=False, verbose_name='密码', max_length=50)
    is_admin = FloatField(default=False, verbose_name='是否管理员')
    sign_date = DateTimeField(default=datetime.now(), verbose_name='注册时间')


class WifiDevice(BaseModel):
    device_name = CharField(verbose_name='设备名', max_length=30)
    class_number = CharField(default=0, verbose_name='教室编号', max_length=10)
    device_number = CharField(verbose_name='设备编号', max_length=10, default=0)
    status = IntegerField(default=0, verbose_name='开关状态')
    degree = IntegerField(default=0, verbose_name='温度')
    gear = CharField(default='低', verbose_name='档位', max_length=10)
    model = CharField(default='无', verbose_name='模式', max_length=10)
    date = DateTimeField(default=datetime.now(), verbose_name='记录时间')
    is_alive = IntegerField(default=0, verbose_name='是否掉线')
    port = IntegerField(default=0, verbose_name='连接端口')


class LoraDevice(BaseModel):
    device_name = CharField(max_length=30, verbose_name='设备名', unique=True)
    class_number = CharField(default=0, verbose_name='教室编号', max_length=10)
    device_number = CharField(verbose_name='设备编号', max_length=30, default=0)
    status = IntegerField(default=0, verbose_name='开关状态')
    data = CharField(max_length=50, verbose_name='上传数据', default=0)
    date = DateTimeField(default=datetime.now(), verbose_name='记录时间')
    is_alive = IntegerField(default=0, verbose_name='是否掉线')
    port = IntegerField(default=0, verbose_name='连接端口')


class RandomCode(BaseModel):
    client_id = CharField(max_length=30, verbose_name='注册id', unique=True)
    client_secret = CharField(max_length=30, verbose_name='注册secret')
    code = CharField(max_length=50, verbose_name='随机code')
    access_token = CharField(max_length=50, verbose_name='access_token')
    refresh_token = CharField(max_length=50, verbose_name='refresh_token')
    date = DateTimeField(default=datetime.now(), verbose_name='记录时间')


def create_tables():
    with database:
        # database.create_tables([User, WifiDevice])
        database.create_tables([RandomCode, Teacher, Course, ClassRoom, Scheduler_Table])


if "__main__"==__name__:
    create_tables()

    # Course.insert(name="数据库",class_name="计算机",session=1,room_id=1,date="2019-9-28",teacher_id=1).execute()
    # Course.insert(name="数据库", class_name="计算机", session=3, room_id=1, date="2019-9-28", teacher_id=1).execute()
    # Course.insert(name="数据库", class_name="计算机", session=5, room_id=1, date="2019-9-29", teacher_id=1).execute()
    # ClassRoom.insert(name="2b301").execute()

