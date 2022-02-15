import time
from concurrent.futures import ThreadPoolExecutor


def fun1():
    print("1开始")
    future = threadlocal.submit(fun2)
    print(future.done())
    print("1结束")


def fun2():
    print("2开始")
    time.sleep(3)
    print("2结束")
    return 1



if __name__ == '__main__':
    lst1 = [4,2]
    lst2 = [1,2]
    lst2 = lst1 + lst2
    print(lst2)