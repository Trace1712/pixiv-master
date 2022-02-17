import threading  # 导入多线程模块
import time  # 导入时间模块
import random  # 导入随机模块


class ThreadFactory:
    def __init__(self):
        self.count = 0  # 使用共享区模拟变量
        self.condition = threading.Condition()

    def reset(self):
        self.count = 0
        self.condition = threading.Condition()

    def producer_run(self, num, func, param):
        if self.condition.acquire():  # 使用条件对象获取锁并锁定
            if self.count >= num:  # 判断共享变量是否已达到上限
                self.condition.wait()  # 当前线程进入阻塞状态
                pass
            else:
                self.count += 1  # 共享变量自增1
                if param is not None:
                    func(param)
                else:
                    func()
                self.condition.notify()  # 唤醒其消费者线程
                pass
            self.condition.release()  # 解除锁定
            # time.sleep(random.randrange(10) / 5)  # 随机休眠n秒

    def consumer_run(self, func, param):
        if self.condition.acquire():  # 使用条件对象获取锁并锁定
            if self.count < 1:  # 判断共享变量是否为空
                self.condition.wait()  # 当前线程进入阻塞状态
                pass
            else:
                self.count -= 1  # 共享变量自减1
                if param is not None:
                    func(param)
                else:
                    func()
                self.condition.notify()  # 唤醒其消费者线程
                pass
            self.condition.release()  # 解除锁定
            time.sleep(random.randrange(10))  # 随机休眠n秒
            pass
        pass
