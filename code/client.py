import socket
import pickle
import json
import myData
import time


def register_name(_socket, _room_name):
    name = input("请为自己注册一个名字：")
    while 1:
        _write_data = myData.MyData(0, name, name, _room_name)
        _write_buff = myData.MyData.data2dict(_write_data)
        _write_buff = json.dumps(_write_buff)
        _write_buff = pickle.dumps(_write_buff)
        _socket.sendall(_write_buff)
        _read_buff = _socket.recv(1024)
        _read_buff = pickle.loads(_read_buff)
        _read_buff = json.loads(_read_buff)
        _read_data = myData.MyData.dict2data(_read_buff)
        if _read_data.msg == "succeed":
            print("注册成功")
            return name
        else:
            name = input("该姓名已被注册请重新输入：")


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
    s.connect((HOST, PORT))  # 要连接的IP与端口
    room_name = input("欢迎使用聊天室软件\n请从（娱乐，工作，生活）选择一个聊天室进入:")
    my_name = register_name(s, room_name)
    """
        发送数据：
        1.创建MyData对象    data = MyData()
        2.将data转换为字典    dict_data = MyData.data2dict(data)
        3.将字典转换为json类型对象    json_data = json.dumps(dict_data)
        4.将json类型对象序列化成一个bytes  bytes_data = pickle.dumps(json_data)
        5.通过socket传递数据  sendall(bytes_data)
    """
    write_data = myData.MyData(2, {'money_sum': 10, 'num': 3, 'packet_name': '%s %s' % (my_name, time.time())}, my_name,
                               room_name)
    write_buff = myData.MyData.data2dict(write_data)
    write_buff = json.dumps(write_buff)
    write_buff = pickle.dumps(write_buff)
    s.sendall(write_buff)
    read_buff = s.recv(1024)
    read_buff = pickle.loads(read_buff)
    read_buff = json.loads(read_buff)
    read_data = myData.MyData.dict2data(read_buff)
    print(read_data)
    write_data = myData.MyData(3, "open", my_name, room_name)
    write_buff = myData.MyData.data2dict(write_data)
    write_buff = json.dumps(write_buff)
    write_buff = pickle.dumps(write_buff)
    s.sendall(write_buff)
    read_buff = s.recv(1024)
    read_buff = pickle.loads(read_buff)
    read_buff = json.loads(read_buff)
    read_data = myData.MyData.dict2data(read_buff)
    print(read_data)
    s.close()  # 关闭连接
