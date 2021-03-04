import threading  # 导入多线程模块
import time  # 导入时间模块
import random  # 导入随机模块

count = 0  # 使用共享区模拟变量
condition = threading.Condition()  # 创建条件对象

# 创建生产者线程类
class Producer(threading.Thread):
    def __init__(self, threadName):  # 构造方法
        threading.Thread.__init__(self)
        self.threadName = threadName
        pass

    def run(self):
        global count  # 引用全局变量
        while True:
            if condition.acquire():  # 使用条件对象获取锁并锁定
                if count >= 10:  # 判断共享变量是否已达到上限
                    print("共享区已满，生产者Producer线程进入阻塞Block状态，停止放入！")
                    condition.wait()  # 当前线程进入阻塞状态
                    pass
                else:
                    count += 1  # 共享变量自增1
                    msg = time.ctime() + ' ' + self.threadName + '生产了1件商品放入共享区，共享区商品总数: ' + str(count)
                    print(msg)
                    condition.notify()  # 唤醒其消费者线程
                    pass
                condition.release()  # 解除锁定
                time.sleep(random.randrange(10) / 5)  # 随机休眠n秒


class Customer(threading.Thread):  # 消费者线程类
    def __init__(self, threadName):  # 构造方法
        threading.Thread.__init__(self)
        self.threadName = threadName
        pass

    def run(self):
        global count  # 引用全局变量
        while True:
            if condition.acquire():  # 使用条件对象获取锁并锁定
                if count < 1:  # 判断共享变量是否为空
                    print("共享区以空，消费者Customer线程进入阻塞Block状态，停止获取！")
                    condition.wait()  # 当前线程进入阻塞状态
                    pass
                else:
                    count -= 1  # 共享变量自减1
                    msg = time.ctime() + ' ' + self.threadName + '消费了一件商品，共享区商品总数: ' + str(count)
                    print(msg)
                    condition.notify()  # 唤醒其消费者线程
                    pass
                condition.release()  # 解除锁定
                time.sleep(random.randrange(10))  # 随机休眠n秒
                pass
            pass
        pass

    pass


if __name__ == '__main__':
    for i in range(2):
        p = Producer('[生产者-0' + str(i + 1) + ']')
        p.start()
        pass
    for i in range(5):
        c = Customer('消费者-' + str(i + 1) + ']')
        c.start()