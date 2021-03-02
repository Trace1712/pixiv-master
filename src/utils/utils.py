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
    name = str(pid) + '.' + suffix
    header = {'Referer': 'https://www.pixiv.net/'}
    req = requests.get(url, headers=header, stream=True)
    if req.status_code == 200:
        open(path + name, 'wb').write(req.content)  # 将内容写入图片
    else:
        print(name + "下载失败")
    del req


def download(picture):
    """
    下载图片
    :param picture: 图片列表
    :return:
    """
    _count = 0
    while len(picture) > 0:
        image_data = picture.pop()
        image = image_data.get_info()
        download_picture(image['url'][0], image['pid'])
        _count += 1
    print(threading.current_thread().getName() +
          "下载完成，共下载图片" + str(_count) + "张")


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


def replace_data(_str: str) -> str:
    """
    替换掉字符串中的非字符内容
    :param _str: 需要处理的字符串
    :return: 返回处理之后的字符串
    """
    _str = _str.replace("false", "'false'")
    _str = _str.replace("null", "'null'")
    _str = _str.replace("true", "'true'")
    # 单引号转双引号
    _str = _str.replace("'", "\"")
    return _str


def join_thread(thread_lst):
    """
    阻塞线程
    :param thread_lst:
    :return:
    """
    for thread_ in thread_lst:
        thread_.join()
