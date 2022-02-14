import requests
import threading
import os
from logger import Logger
from ippool import *

logger = Logger("hmk").get_log()


def download_picture(url, pid, path, suffix="jpg"):
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
    if not os.path.exists(path):
        os.mkdir(path)
    if req.status_code == 200:
        open(path + name, 'wb').write(req.content)  # 将内容写入图片
        logger.info("{} download success".format(name))
    else:
        logger.info("{} download fail".format(name))
    del req


def download(picture, path="..\\..\\picture\\"):
    """
    下载图片
    :param path: 图片路径
    :param picture: 图片列表
    :return:
    """
    _count = 0
    while len(picture) > 0:
        image_data = picture.pop()
        image = image_data.get_info()
        download_picture(image['url'][0], image['pid'], path)
        _count += 1
    logger.info("{} download finish, downloaded {} pictures".format(threading.current_thread().getName(), _count))


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
    logger.info("{} is runnning function {}".format(threading.current_thread().getName(), function.__name__))
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


def request(headers, cookie, url, use_proxy, ip=None):
    """
    封装请求函数
    :param ip:
    :param headers: 浏览头
    :param cookie: cookie
    :param url: url
    :param use_proxy:是否用代理IP
    :return:
    """
    try:
        if not use_proxy:
            req = requests.get(url, headers=headers, cookies=cookie).text
            ip = None
        else:
            ip = get_ip() if not ip else ip
            proxies = {
                'http': 'http://' + ip,
                # 'https': 'https://' + ip
            }
            req = requests.get(url, headers=headers, cookies=cookie, proxies=proxies, allow_redirects=False).text
        return req, ip
    except:
        logger.info("网络错误")


if __name__ == '__main__':
    path = "..\\..\\picture\\20210306"
    if not os.path.exists(path):
        os.mkdir(path)
