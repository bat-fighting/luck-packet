import numpy as np
from multiprocessing import Process
from multiprocessing import Pool
import os
import queue


def clientInit(name="default"):
    print("i'm client %d" % name)
    p_pid = os.getppid()
    print(p_pid)


def init(client_num=1):
    for i in range(client_num):
        p = Process(target=clientInit, args=(i + 1,))
        p.start()


def sendPacket(money_sum, num):
    points = [0]
    packets = []
    temp_sum = 0
    if money_sum < num * 0.01:
        print("单个红包金额不能小于0.01")
        return
    for i in range(num - 1):
        points.append(np.random.random_sample())
    points.sort()
    for i in range(len(points) - 1):
        temp = round((points[i + 1] - points[i]) * money_sum, 2)
        if temp == 0:
            temp = 0.01
        packets.append(temp)
        temp_sum += temp
    temp = round(money_sum - temp_sum, 2)
    if temp > 0:
        packets.append(temp)
        return packets
    else:
        return sendPacket(money_sum, num)


def openPacket():
    print()


if __name__ == "__main__":

    init(10)
    packet_queue = queue.Queue()
    packet = sendPacket(200, 10)
    if packet:
        packet_queue.put(packet)
    else:
        print("error")
    print(packet_queue.get(0))
