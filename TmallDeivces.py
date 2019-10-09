# -*- coding:utf-8 -*-
# Author: cmzz
# @Time :2019/10/2

#  天猫的设备在这里添加
# 支持的 deviceType
# 电视	television
# 灯	light
# 空调	aircondition
# 空气净化器	airpurifier
# 插座	outlet
# 开关	switch
# 扫地机器人	roboticvacuum
# 窗帘	curtain
# 加湿器	humidifier
# 风扇	fan
# 暖奶器	milkregulator
# 豆浆机	soymilkmaker
# 电热水壶	kettle
# 饮水机	waterdispenser
# 摄像头	camera
# 路由器	router
# 电饭煲	cooker
# 热水器	waterheater
# 烤箱	oven
# 净水器	waterpurifier
# 冰箱	fridge
# 机顶盒	STB
# 传感器	sensor
# 洗衣机	washmachine
# 智能床	smartbed
# 香薰机	aromamachine
# 窗	window
# 抽油烟机	kitchenventilator
# 指纹锁	fingerprintlock
# 万能遥控器	telecontroller
# 洗碗机	dishwasher
# 除湿机	dehumidifier
# 干衣机	dryer
# 壁挂炉	wall-hung-boiler
# 微波炉	microwaveoven
# 取暖器	heater
# 驱蚊器	mosquitoDispeller
# 跑步机	treadmill
# 智能门控(门锁)	smart-gating
# 智能手环	smart-band
# 晾衣架	hanger
# 血压仪	bloodPressureMeter
# 血糖仪	bloodGlucoseMeter
# 电热毯	blanket


# json 里面的devices为list，deviceId前一个{ 为开始，extension2后第二个} 为结束，之间用,隔开。
# 天猫文档 https://doc-bot.tmall.com/docs/doc.htm?spm=0.7629140.0.0.79f81780t0v6tN&treeId=393&articleId=108271&docType=1
devices = '''{
                      "header":{
                          "namespace":"AliGenie.Iot.Device.Discovery",
                          "name":"DiscoveryDevicesResponse",
                          "messageId":"1bd5d003-31b9-476f-ad03-71d471922820",
                          "payLoadVersion":1
                       },
                       "payload":{
                          "devices":[


                          {
                          "deviceId":"fan-2",
                          "deviceName":"2号风扇",
                          "deviceType":"fan",
                          "zone":"",          
                          "brand":"",
                          "model":"",     
                          "icon":"https://git.cn-hangzhou.oss-cdn.aliyun-inc.com/uploads/aicloud/aicloud-proxy-service/41baa00903a71c97e3533cf4e19a88bb/image.png",
                          "properties":[{
                            "name":"color",
                            "value":"Red"
                           }
                           ],
                          "actions":[
                            "TurnOn",
                            "TurnOff",
                            "SetBrightness",       
                            "AdjustBrightness",     
                            "SetTemperature",
                            "Query"        
                         ],
                          "extensions":{
                             "extension1":"",
                             "extension2":""
                          }
                         },


                         {
                          "deviceId":"lamp",
                          "deviceName":"灯",
                          "deviceType":"light",
                          "zone":"",          
                          "brand":"",
                          "model":"",     
                          "icon":"https://git.cn-hangzhou.oss-cdn.aliyun-inc.com/uploads/aicloud/aicloud-proxy-service/41baa00903a71c97e3533cf4e19a88bb/image.png",
                          "properties":[{
                            "name":"color",
                            "value":"Red"
                           }
                           ],
                          "actions":[
                            "TurnOn",
                            "TurnOff",
                            "SetBrightness",       
                            "AdjustBrightness",     
                            "SetTemperature",
                            "Query"        
                         ],
                          "extensions":{
                             "extension1":"",
                             "extension2":""
                          }
                         },   



                         ]
                       }
                    }'''