# -*- coding:utf-8 -*-
# Author: cmzz
# @Time :2019/9/2
from datetime import datetime

from peewee import MySQLDatabase, Model, CharField, FloatField, IntegerField, DateTimeField, CompositeKey

database = MySQLDatabase('tornado_db', **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'port': 3306,
                                          'user': 'tornado_user', 'password': 'ciel2019'})


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(unique=True, verbose_name='用户名', max_length=50)
    password = CharField(null=False, verbose_name='密码', max_length=50)
    is_admin = FloatField(default=False, verbose_name='是否管理员')
    sign_date = DateTimeField(default=datetime.now(), verbose_name='注册时间')


class WifiDevice(BaseModel):
    device_name = CharField(verbose_name='设备名', max_length=10)
    class_number = CharField(default=0, verbose_name='教室编号', max_length=10)
    device_number = CharField(verbose_name='设备编号', max_length=10, default=0)
    status = IntegerField(default=0, verbose_name='开关状态')
    degree = IntegerField(default=0, verbose_name='温度')
    gear = CharField(default='低', verbose_name='档位', max_length=10)
    model = CharField(default='无', verbose_name='模式', max_length=10)
    date = DateTimeField(default=datetime.now(), verbose_name='记录时间')
    is_alive = IntegerField(default=0, verbose_name='是否掉线')
    port = IntegerField(default=0, verbose_name='连接端口')

    # class Meta:
    #     primary_key = CompositeKey('class_number', 'device_number')


# class LampDevice(BaseModel):
#     device_name = CharField(verbose_name='设备名', max_length=10, default='lamp')
#     device_number = CharField(verbose_name='设备编号', max_length=30, default=0)
#     class_number = CharField(default=0, verbose_name='教室编号', max_length=10)
#     status = IntegerField(default=0, verbose_name='开关状态')
#     date = DateTimeField(default=datetime.now(), verbose_name='记录时间')
#     is_alive = IntegerField(default=0, verbose_name='是否掉线')
#     port = IntegerField(default=0, verbose_name='连接端口')


# class FanDevice(BaseModel):
#     device_name = CharField(verbose_name='设备名', max_length=10, default='fan')
#     device_number = CharField(verbose_name='设备编号', max_length=10, default=0)
#     class_number = CharField(default=0, verbose_name='教室编号', max_length=10)
#     status = IntegerField(default=0, verbose_name='开关状态')
#     gear = CharField(default='低', verbose_name='档位', max_length=10)
#     date = DateTimeField(default=datetime.now(), verbose_name='记录时间')
#     is_alive = IntegerField(default=0, verbose_name='是否掉线')
#     port = IntegerField(default=0, verbose_name='连接端口')


class LoraDevice(BaseModel):
    device_name = CharField(max_length=30, verbose_name='设备名', unique=True)
    class_number = CharField(default=0, verbose_name='教室编号', max_length=10)
    device_number = CharField(verbose_name='设备编号', max_length=30, default=0)
    status = IntegerField(default=0, verbose_name='开关状态')
    data = CharField(max_length=50, verbose_name='上传数据', default=0)
    date = DateTimeField(default=datetime.now(), verbose_name='记录时间')
    is_alive = IntegerField(default=0, verbose_name='是否掉线')
    port = IntegerField(default=0, verbose_name='连接端口')


def create_tables():
    with database:
        # database.create_tables([User, WifiDevice])
        database.create_tables([LoraDevice])


if __name__ == '__main__':
    create_tables()
