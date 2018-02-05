from multiprocessing import Pool
import time


class someClass(object):

    def __init__(self):
        pass

    def set_pool(self):
        self.pool = Pool(10)

    def get_pool(self):
        return self.pool

    def f(self, x):
        time.sleep(2)
        print(x)

    def go(self, _pool):
        pool = _pool
        pool.map(self.f, range(20))
        """
        for i in range(17):
            pool.apply_async(self.f, (i, i - 1))
        pool.close()
        pool.join()
        """


def fun():
    print(num)


if __name__ == "__main__":
    sc = someClass()
    # sc.go()
    sc.set_pool()
    sc.get_pool
    num = 10
    fun()
    list = [1, 2, 3, 4, 5]
    d = {'name': 'jack'}
    list.append(d)
    print(list[-1])
    print(list)
