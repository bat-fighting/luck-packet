# encoding = utf-8
import time


class MyData(object):

    def __init__(self, _type=None, _msg=None, _come=None, _to=None,
                 _time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
        self._type = _type
        self._msg = _msg
        self._come = _come
        self._to = _to
        self._time = _time

    def __str__(self):
        return str(MyData.data2dict(self))

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value

    @property
    def come(self):
        return self._come

    @come.setter
    def come(self, value):
        self._come = value

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, value):
        self._to = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @staticmethod
    def data2dict(_data):
        return {
            "type": _data.type,
            "msg": _data.msg,
            "come": _data.come,
            "to": _data.to,
            "time": _data.time
        }

    @staticmethod
    def dict2data(_dict):
        return MyData(_dict['type'],
                      _dict['msg'],
                      _dict['come'],
                      _dict['to'],
                      _dict['time'])


if __name__ == "__main__":
    data = MyData()
    b = MyData(1, 2, 3, 4)
    print(b)
    b = MyData.data2dict(b)
    print(b)
    bb = MyData.dict2data(b)
    print(bb)
    print(bb.time)
