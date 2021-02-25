import requests
import threading
import time


def download_picture(url, pid, suffix="jpg", path="..\\picture\\"):
    """
    图片下载器
    :param path: 保存文件夹路径
    :param suffix: 保存后缀
    :param pid: 图片id
    :param url: 图片地址
    :return:
    """
    name = str(pid) + suffix
    header = {'Referer': 'https://www.pixiv.net/'}
    req = requests.get(url, headers=header, stream=True)
    if req.status_code == 200:
        open(path + name, 'wb').write(req.content)  # 将内容写入图片
    else:
        print(name + "下载失败")
    del req


def create_thread(function, *args):
    """
    线程启动器
    :param args: 方法参数
    :param function:方法
    :return:
    """
    if args is None:
        t = threading.Thread(target=function)
    else:
        # 有参处理
        result = list()
        for arg in args:
            result.append(arg)
        t = threading.Thread(target=function, args=tuple(result))
    print(threading.current_thread().getName() + "正在执行" + str(function.__name__))
    t.start()
    return t
