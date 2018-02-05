# encoding=utf-8
from multiprocessing import Pool
from multiprocessing import Process
import time
import queue
import numpy as np


# 服务器类Server
class Server(object):
    packet_queue = queue.Queue()

    # 初始化 Server pool_num参数制定服务器进程池大小
    def __init__(self):
        pass

    # 发红包函数 指定 红包总金额 和 红包个数
    def recv_packet(self, money_sum, num):
        points = [0.]
        packet_list = []
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
            packet_list.append(temp)
            temp_sum += temp
        temp = round(money_sum - temp_sum, 2)
        if temp > 0:
            packet_list.append(temp)
            self.packet_queue.put(packet_list)
            # self.insert_pool()
        else:
            self.recv_packet(money_sum, num)

    def get_packet(self, packet_list):
        print(packet_list)
        time.sleep(3)

    def insert_pool(self):
        pool = Pool(10)
        list_len = self.packet_queue.qsize()
        for i in range(list_len):
            packet_list = self.packet_queue.get()
            pool.apply_async(self.get_packet, (packet_list,))
        pool.close()
        pool.join()


class Client(object):

    def __init__(self, _server):
        self.server = _server

    def func(self):
        print(self.server.packet_queue.qsize())

    def send_packet(self, money_sum, num):
        self.server.recv_packet(money_sum, num)


def my_func(name):
    print("i'm %s" % name)
    time.sleep(2)
    print("end")


if __name__ == "__main__":
    # server = Server()
    pool = Pool(10)
    client = []
    for i in range(10):
        p = Process(target=my_func, args=(i,))
        p.start()
