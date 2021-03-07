import requests
import threading
import time
from utils.ippool import test_ip
import os
from utils.logger import Logger

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
        print(name + "下载完成")
    else:
        print(name + "下载失败")
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


def get_ip():
    """
    获取代理IP
    :return:
    """
    flag = 0
    while True:
        url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
        req = requests.get(url)
        if req.status_code == 200:
            flag += 1
            result = test_ip(req.text)
            if result != "请求超时":
                print("获取到可用IP")
                return req.text
            else:
                print("IP无效,重新获取")
        else:
            print("请求IP失败,code为%s" % (str(req.status_code)))
        if flag == 3:
            print("失败次数过多无钱了,请联系客服QAQ")
            break


def request(headers, cookie, url, use_proxy):
    """
    封装请求函数
    :param headers: 浏览头
    :param cookie: cookie
    :param url: url
    :param use_proxy:是否用代理IP
    :return:
    """
    try:
        if not use_proxy:
            req = requests.get(url, headers=headers, cookies=cookie).text
        else:
            ip = get_ip()
            proxies = {
                'http': 'http://' + ip,
                # 'https': 'https://' + proxy
            }
            req = requests.get(url, headers=headers, cookies=cookie, proxies=proxies).text
        return req
    except:
        logger.info("网络错误")


if __name__ == '__main__':
    path = "..\\..\\picture\\20210306"
    if not os.path.exists(path):
        os.mkdir(path)
