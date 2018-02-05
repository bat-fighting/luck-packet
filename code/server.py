# encoding=utf-8

import socket
import select
from multiprocessing import Pool
import time
import threading
import pickle
import json
import myData
import chatRoom
import numpy as np
import queue

client_list = []


def init_server(ip="127.0.0.1", port=8888):
    # 创建socket (AF_INET:IPv4, SOCK_STREAM:面向流的TCP协议)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定本机IP和端口
    s.bind((ip, port))
    # 设置监听队列
    s.listen(5)
    print('Server is running...')
    return s


def rec_data(_client_sock):
    read_buff = _client_sock.recv(1024)
    if read_buff:
        read_buff = pickle.loads(read_buff)
        read_buff = json.loads(read_buff)
        read_data = myData.MyData.dict2data(read_buff)
        return read_data
    else:
        return


def send_data(_sock, _data):
    write_buff = myData.MyData.data2dict(_data)
    write_buff = json.dumps(write_buff)
    write_buff = pickle.dumps(write_buff)
    _sock.sendall(write_buff)


'''
:type 0 注册用户消息，1 普通消息， 2 发红包消息， 3 抢红包消息
'''


def execute(_data, _sock, _room):
    if _data.type == 0:
        t = threading.Thread(target=enter_room, args=(_data, _sock, _room))
        t.setDaemon(True)
        t.start()
    elif _data.type == 1:
        t = threading.Thread(target=messaging, args=(_data, _sock, _room))
        t.setDaemon(True)
        t.start()
    elif _data.type == 2:
        t = threading.Thread(target=send_packet, args=(_data, _sock, _room))
        t.setDaemon(True)
        t.start()
    elif _data.type == 3:
        t = threading.Thread(target=open_packet, args=(_data, _sock, _room))
        t.setDaemon(True)
        t.start()


def enter_room(_data, _sock, _room):
    _str = _data.msg
    client_member = {'fd': _sock, 'name': _data.msg}
    for __room in _room:
        if _data.to == __room.name:
            for __member in __room.member:
                if _str == __member['name']:
                    ret = myData.MyData(_msg="re-registration")
                    send_data(_sock, ret)
                    break
            ret = myData.MyData(_msg="succeed")
            send_data(_sock, ret)
            print("一个新用户进入 %s 聊天室。" % _data.to)
            __room.member.append(client_member)


def messaging(_data, _sock, _room):
    for __room in _room:
        if _data.to == __room.name:
            for __member in __room.member:
                if _sock == __member['fd']:
                    continue
                _data = myData.MyData(1, _data.msg, __room.name, __member['name'])
                send_data(__member['fd'], _data)


def packet_init(money_sum, num):
    points = [0.]
    _packet_queue = queue.Queue()
    temp_sum = 0
    if money_sum < num * 0.01:
        print("单个红包金额不能小于0.01")
        return
    for _ in range(num - 1):
        points.append(np.random.random_sample())
    points.sort()
    for i in range(len(points) - 1):
        temp = round((points[i + 1] - points[i]) * money_sum, 2)
        if temp == 0:
            temp = 0.01
        _packet_queue.put(temp)
        temp_sum += temp
    temp = round(money_sum - temp_sum, 2)
    if temp > 0:
        _packet_queue.put(temp)
        return _packet_queue
    else:
        packet_init(money_sum, num)


def packet_inform(_room):
    if _room:
        for __member in _room.member:
            _data = myData.MyData(1, "红包 %s 准备就绪" % _room.database[-1]['name'], "server", __member['name'])
            send_data(__member['fd'], _data)
    else:
        print("None")


def send_packet(_data, _sock, _room):
    _packet_queue = packet_init(_data.msg['money_sum'], _data.msg['num'])
    for __room in _room:
        if _data.to == __room.name:
            _packet = {'name': _data.msg['packet_name'], 'resource': _packet_queue}
            __room.database.append(_packet)
            packet_inform(__room)
            print(__room.database)


def open_packet(_data, _sock, _room):
    for __room in _room:
        if _data.to == __room.name:
            _packet_queue = __room.database[0]['resource']
            _packet = _packet_queue.get()
            __data = myData.MyData(1, _packet, "server", _data.come)
            send_data(_sock, __data)
    pass


if __name__ == "__main__":
    server_sock = init_server()
    recreation_room = chatRoom.ChatRoom("娱乐")
    work_room = chatRoom.ChatRoom("工作")
    livelihood_room = chatRoom.ChatRoom("生活")
    chat_room = [recreation_room, work_room, livelihood_room]
    inputs = [server_sock]
    outputs = []
    while True:
        readable, writeable, exceptional = select.select(inputs, outputs, inputs)
        if not (readable or writeable or exceptional):
            continue

        for s in readable:
            if s == server_sock:
                client_sock, address = server_sock.accept()  # 接收一个新连接
                inputs.append(client_sock)
                outputs.append(client_sock)
            else:
                data = rec_data(s)  # 处理连接
                if data:
                    print(data)
                    execute(data, s, chat_room)
                else:
                    for room in chat_room:
                        for _member in room.member:
                            if s == _member['fd']:
                                print('%s离开了聊天室' % _member['name'])
                            room.member.remove(_member)
                            break
                    client_sock.close()
                    inputs.remove(client_sock)
                    outputs.remove(client_sock)
    server_sock.close()
