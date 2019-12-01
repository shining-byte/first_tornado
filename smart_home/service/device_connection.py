import re
# from service.device_control import DeviceController, DeviceNotExistException, DeviceNotConnectException
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from models.smartroom import WifiDevice,ClassRoom

from config import logging
TCP_CONNECTION = {}

class TcpHandler(TCPServer):
    """
    tcp 连接
    """
    global TCP_CONNECTION

    async def handle_stream(self, stream, address):
        info_dict = {}
        try:
            while True:
                msg = await stream.read_bytes(2048, partial=True)
                # print(msg)
                # logging.info('记录tcp连接:{}'.format(msg))
                msg = msg.decode('utf-8')
                # logging.info('msg1{}'.format(msg))
                for msg in re.findall('({.*?})', msg):
                    print(msg)
                    # logging.info(msg, '-----------------------------msg----------------------')
                    # print(msg, '------------------------------msg----------------------')
                    msg = eval(msg)
                    # logging.info('msg{}'.format(msg))
                    # 掉线处理要用到的port
                    msg['port'] = address[1]
                    # 判断是否为初次建立连接,发送heartbeat
                    # 用规定的指令设备名和课室创建key
                    # 处理返回指令
                    if(msg['device_name']+msg['class'] in info_dict.keys()):  # 判断是否已经连接,这里匹配，应该为 {'device_name': 'fan-lamp-curtain', 'class': 'G511', 'fan': '3', 'lamp': '3', 'curtain': '1'}
                        # info_dict根据device_name和class来存放整一个msg
                        if (msg == info_dict[msg['device_name']+msg['class']]):  # 判断是否心跳包
                            # print(info_dict[msg['device_name']])
                            print('状态相同,心跳包')
                            # logging.info('心跳包')
                            continue
                        else:
                            # 下发指令或者android更改设备状态返回信息
                            # logging.info('更新操作{}'.format(msg))

                            # if (msg['device_name'] == 'fan-lamp-curtain'):
                            if (re.findall('lamp|fan|curtain', str(msg))):
                                print('风扇更新操作')
                                match_list = re.findall('\w*-\d', str(msg))
                                # 匹配lamp-1,fan-1...
                                for i in match_list:
                                    # i: ['lamp-1', 'curtain-1'.....]
                                    update = WifiDevice.update(status=msg[i]). \
                                        where(
                                        (WifiDevice.device_number == i) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # 更新info_dict信息里面单个信息
                                    info_dict[msg['device_name']+msg['class']][i] = msg[i] # msg[i] 为lamp-1的 ‘1’ or ‘0’                            print('更新操作')
                            # elif (msg['device_name'] == 'fan-lamp'):
                            #
                            #     match_list = re.findall('\w*-\d', str(msg))
                            #     # 匹配lamp-1,fan-1...
                            #     for i in match_list:
                            #         update = WifiDevice.update(status=msg[i]). \
                            #             where(
                            #             (WifiDevice.device_number == i) & (WifiDevice.class_number == msg['class']))
                            #         update.execute()
                            #         # 更新info_dict信息里面单个信息
                            #         info_dict[msg['device_name']+msg['class']][i] = msg[i] # msg[i] 为lamp-1的 ‘1’ or ‘0’
                            elif (re.findall('air', msg['device_name'])):
                                print('空调更新')
                                # logging.info('air{}'.format(msg))
                                # logging.info('info_dict{}'.format(info_dict[msg['device_name']]))
                                if ('degree' in msg.keys() and 'status' in msg.keys() and 'gear' in msg.keys() and 'model' in msg.keys()):
                                    # logging.info('更新全部')
                                    # logging.info(msg)
                                    update = WifiDevice.update(degree=msg['degree'], status=msg['status'], gear=msg['gear'], model=msg['model']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    info_dict[msg['device_name']+msg['class']]['degree'] = msg['degree']
                                    info_dict[msg['device_name']+msg['class']]['status'] = msg['status']
                                    info_dict[msg['device_name']+msg['class']]['gear'] = msg['gear']
                                    info_dict[msg['device_name']+msg['class']]['model'] = msg['model']
                                # 单独更新
                                elif('degree' in msg.keys()):
                                    update = WifiDevice.update(degree=msg['degree']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # logging.info('更新degree')
                                    info_dict[msg['device_name']+msg['class']]['degree'] = msg['degree']
                                elif ('status' in msg.keys()):
                                    update = WifiDevice.update(status=msg['status']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # logging.info('更新status')
                                    info_dict[msg['device_name']+msg['class']]['status'] = msg['status']
                                elif ('gear' in msg.keys()):
                                    update = WifiDevice.update(gear=msg['gear']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # logging.info('更新gear')
                                    info_dict[msg['device_name']+msg['class']]['gear'] = msg['gear']
                                elif ('model' in msg.keys()):
                                    update = WifiDevice.update(gear=msg['model']). \
                                        where(
                                        (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # logging.info('更新model')
                                    info_dict[msg['device_name']+msg['class']]['model'] = msg['model']
                            elif (re.findall('controller', msg['device_name'])):
                                match_list = re.findall('console-\d', str(msg))
                                # 匹配lamp-1,fan-1...
                                for i in match_list:
                                    update = WifiDevice.update(status=msg[i]). \
                                        where(
                                        (WifiDevice.device_number == i) & (WifiDevice.class_number == msg['class']))
                                    update.execute()
                                    # 更新info_dict信息里面单个信息
                                    info_dict[msg['device_name'] + msg['class']][i] = msg[i]
                            elif (re.findall('switch', msg['device_name'])):
                                # match_list = re.findall('switch-\d', str(msg))
                                print('开关动作')
                                # 匹配lamp-1,fan-1...
                                devices = WifiDevice.select() \
                                    .where((WifiDevice.class_number == msg['class']) & (
                                            WifiDevice.device_name == msg['device_name'])).execute()
                                list_ = [device.device_number for device in devices]
                                if msg['status'] == '1':
                                    print('action ==1 ')
                                    await TCP_CONNECTION[msg['device_name'] + msg['class']].write(b'''{'devices_name': 'fan-lamp-curtain', 'class': 'C1004', 'lamp-1': '0', 'lamp-2': '0','lamp-3': '0', 'fan-1': '0', 'fan-2': '0', 'curtain-1':'0'}''')
                                    # await device_controller.turn_devices_on(list_)
                                    # for i in list_:
                                    #     pass
                                        # await DeviceController(i, msg['class']).turn_devices_on(list_)
                                elif msg['status'] == '0':
                                    await TCP_CONNECTION[msg['device_name'] + msg['class']].write(b'''{'device_name': 'fan-lamp-curtain', 'class': 'C1004', 'lamp-1': '0', 'lamp-2': '0','lamp-3': '0', 'fan-1': '0', 'fan-2': '0', 'curtain-1':'0'}''')
                                    print('0')
                                    # for i in list_:
                                    #     pass
                                        # await DeviceController(i, msg['class']).turn_devices_off(list_)
                                update = WifiDevice.update(status=msg['status']). \
                                    where(
                                    (WifiDevice.device_name == msg['device_name']) & (
                                                WifiDevice.class_number == msg['class']))
                                update.execute()
                                    # 更新info_dict信息里面单个信息
                                info_dict[msg['device_name'] + msg['class']]['status'] = msg['status']
                    else:
                        print('第一次连接')
                        # logging.info('第一次连接')
                        return_dict = {}
                        TCP_CONNECTION[msg['device_name'] + msg['class']] = stream
                        # stream.write(bytes(msg, encoding='utf-8'))
                        # 根据初次连接上发的指令，记录到数据库
                        if ('lamp' in msg.keys() and 'fan' in msg.keys() and 'curtain' in msg.keys()):
                            print('同时存在')
                            logging.info('三个设备同时存在')
                            for i in range(1, int(msg['fan']) + 1):
                                fan = WifiDevice.get_or_create(device_number='fan-{}'.format(i),
                                                               class_number=msg['class'],
                                                               defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                         'port': address[1]})
                                return_dict['fan-{}'.format(i)] = fan[0].status
                            for j in range(1, int(msg['lamp']) + 1):
                                lamp = WifiDevice.get_or_create(device_number='lamp-{}'.format(j),
                                                                class_number=msg['class'],
                                                                defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                          'port': address[1]})
                                return_dict['lamp-{}'.format(j)] = lamp[0].status
                            for k in range(1, int(msg['curtain']) + 1):
                                curtain = WifiDevice.get_or_create(device_number='curtain-{}'.format(k),
                                                                   class_number=msg['class'],
                                                                   defaults={'device_name': msg['device_name'],
                                                                             'is_alive': 1,
                                                                             'port': address[1]})
                                return_dict['curtain-{}'.format(k)] = curtain[0].status
                        elif ('lamp' in msg.keys() and 'fan' in msg.keys()):
                            print('lamp和fan同时存在')
                            logging.info('风扇,灯同时存在')
                            for i in range(1, int(msg['fan']) + 1):
                                fan = WifiDevice.get_or_create(device_number='fan-{}'.format(i),
                                                               class_number=msg['class'],
                                                               defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                         'port': address[1]})
                                return_dict['fan-{}'.format(i)] = fan[0].status
                            for j in range(1, int(msg['lamp']) + 1):
                                lamp = WifiDevice.get_or_create(device_number='lamp-{}'.format(j),
                                                                class_number=msg['class'],
                                                                defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                          'port': address[1]})
                                return_dict['lamp-{}'.format(j)] = lamp[0].status
                        elif ('fan' in msg.keys()):
                            print('fan存入数据库操作')
                            for i in range(1, int(msg['fan']) + 1):
                                fan = WifiDevice.get_or_create(device_number='fan-{}'.format(i),
                                                               class_number=msg['class'],
                                                               defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                         'port': address[1]})
                                return_dict['fan-{}'.format(i)] = fan[0].status
                                print(fan[0].status)
                                print(msg.keys())
                        elif ('lamp' in msg.keys()):
                            print('lamp存入数据库')
                            for j in range(1, int(msg['lamp']) + 1):
                                lamp = WifiDevice.get_or_create(device_number='lamp-{}'.format(j),
                                                                class_number=msg['class'],
                                                                defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                          'port': address[1]})
                                return_dict['lamp-{}'.format(j)] = lamp[0].status

                        elif ('curtain' in msg.keys()):
                            print('curtain存入数据库')
                            for j in range(1, int(msg['curtain']) + 1):
                                curtain = WifiDevice.get_or_create(device_number='curtain-{}'.format(j),
                                                                class_number=msg['class'], device_name=msg['device_name'],
                                                                defaults={'is_alive': 1,
                                                                          'port': address[1]})
                                return_dict['curtain-{}'.format(j)] = curtain[0].status
                                print(curtain[0].port)

                        elif (re.findall('air', msg['device_name'])):
                            print('空调')
                            # number = re.findall('\d', msg['device_name'])[0]
                            # for k in msg['air']:
                            air = WifiDevice.get_or_create(device_name=msg['device_name'],
                                                           class_number=msg['class'], device_number=msg['device_name'],
                                                           defaults={'degree': '25', 'is_alive': 1, 'gear': '1',
                                                                     'model': '1',
                                                                     'port': address[1]})
                            return_dict['status'] = air[0].status
                            return_dict['degree'] = str(air[0].degree)
                            return_dict['gear'] = air[0].gear
                            return_dict['model'] = air[0].model
                        elif (re.findall('controller', msg['device_name'])):
                            for i in range(1, int(msg['console']) + 1):
                                controller = WifiDevice.get_or_create(device_number='console-{}'.format(i),
                                                         class_number=msg['class'],
                                                         defaults={'device_name': msg['device_name'], 'is_alive': 1,
                                                                   'port': address[1]})
                                return_dict['console-{}'.format(i)] = controller[0].status
                        # 开关
                        elif(re.findall('switch', msg['device_name'])):
                            print('开关')
                            switch = WifiDevice.get_or_create(device_name=msg['device_name'],
                                                           class_number=msg['class'], device_number=msg['device_name'],
                                                           defaults={'is_alive': 1, 'port': address[1]})
                            return_dict['status'] = switch[0].status
                        ClassRoom.get_or_create(name=msg['class'])
                        return_dict['device_name'] = msg['device_name']
                        return_dict['class'] = msg['class']
                        # logging.info('info_dict{}'.format(info_dict.values()))
                        # 硬件死机重连返回必要信息,取消,硬件找到存储信息的方法了.
                        # print('return_dict:{}'.format(return_dict))
                        await stream.write(b"{'heartBeat'}")
                        # logging.info('return_dict{}'.format(return_dict))
                        # await stream.write(bytes(str(return_dict), encoding='utf-8'))
                        return_dict['port'] = msg['port']
                        info_dict[msg['device_name']+msg['class']] = return_dict
                        del return_dict
                        # 重连修改连接端口号
                        update = WifiDevice.update(port=address[1], is_alive=1).where(
                            (WifiDevice.device_name == msg['device_name']) & (WifiDevice.class_number == msg['class']))
                        update.execute()
                    # else:
                    #     # 处理单片机返回非json数据
                    #     logging.info("处理单片机返回非json数据：{}".format(msg))
                    #     print(msg)
        except Exception as e:
            print('错误信息{}'.format(e))
            # 掉线处理

            for value in info_dict.values():
                # value = eval(value)
                print(value, '掉线')
                if (address[1] in value.values()):
                    print('处理')
                    # print(value['device_name'], value['class'])
                    # wifi设备掉线,数据更改数据库设备状态
                    update = WifiDevice.update(is_alive=0).where(WifiDevice.port == address[1])
                    update.execute()
            # wifi tcp断开后会出错, 根据address查询数据库并修改状态
            # print('掉线')

            # print("TcpHandler---------{}".format(e))


async def heartbeat():
    """
    心跳包
    :return:
    """
    try:
        for key, value in TCP_CONNECTION.items():
            print('{}发送心跳包'.format(key))
            # logging.info('{}发送心跳包'.format(key))
            await value.write(b"{'heartBeat'}")
            # await i.write(b"heartBeat")
    except Exception as e:
        TCP_CONNECTION.pop(key)

        print('出错设备号{},错误信息{}'.format(key, e))
