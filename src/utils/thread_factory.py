import threading  # 导入多线程模块
import time  # 导入时间模块
import random  # 导入随机模块

# count = 0  # 使用共享区模拟变量
# condition = threading.Condition()  # 创建条件对象


def producer_run(condition, num, thread_name, func, param):
    global count
    if condition.acquire():  # 使用条件对象获取锁并锁定
        if count >= num:  # 判断共享变量是否已达到上限
            print("共享区已满，生产者Producer线程进入阻塞Block状态，停止放入！")
            condition.wait()  # 当前线程进入阻塞状态
            pass
        else:
            count += 1  # 共享变量自增1
            if param is not None:
                func(param)
            else:
                func()
            msg = time.ctime() + ' ' + thread_name + '生产了1件商品放入共享区，共享区商品总数: ' + str(count)
            print(msg)
            condition.notify()  # 唤醒其消费者线程
            pass
        condition.release()  # 解除锁定
        # time.sleep(random.randrange(10) / 5)  # 随机休眠n秒


def consumer_run(condition, thread_name, func, param):
    global count  # 引用全局变量
    if condition.acquire():  # 使用条件对象获取锁并锁定
        if count < 1:  # 判断共享变量是否为空
            print("共享区以空，消费者Customer线程进入阻塞Block状态，停止获取！")
            condition.wait()  # 当前线程进入阻塞状态
            pass
        else:
            count -= 1  # 共享变量自减1
            if param is not None:
                func(param)
            else:
                func()
            msg = time.ctime() + ' ' + thread_name + '消费了一件商品，共享区商品总数: ' + str(count)
            print(msg)
            condition.notify()  # 唤醒其消费者线程
            pass
        condition.release()  # 解除锁定
        time.sleep(random.randrange(10))  # 随机休眠n秒
        pass
    pass
