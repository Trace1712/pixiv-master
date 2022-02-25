import os
from utils.logger import Logger
from utils.ippool import *

logger = Logger("pixiv").get_log()


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
    try:
        req = requests.get(url, headers=header)
    except Exception as e:
        logger.info("{} download fail".format(name, e))

    if req.status_code == 200:
        if not os.path.exists(path):
            os.mkdir(path)
        fp = open(path + name, 'wb')
        fp.write(req.content)  # 将内容写入图片
        fp.close()
        logger.info("{} download success".format(url))
    else:
        logger.info("{} download fail".format(url))
    del req


def download(picture, path="..\\picture\\"):
    """
    下载图片
    :param path: 图片路径
    :param picture: 图片列表
    :return:
    """
    image_data = picture
    image = image_data.get_info()
    download_picture(image['url'][0], image['pid'], path)

    logger.info("download finish {}".format(image['pid']))


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
        else:
            # ip = get_ip() if not ip else ip
            proxies = {
                'http': 'http://' + ip,
                'https': 'https://' + ip
            }
            req = requests.get(url, headers=headers, cookies=cookie, proxies=proxies, allow_redirects=False).text
        return req
    except:
        logger.info("network error, req failed")


if __name__ == '__main__':
    download_picture("https://i.pximg.net/img-original/img/2022/02/16/21/00/12/96303074_p0.png", '96303074',
                     '..\\..\\picture\\')
