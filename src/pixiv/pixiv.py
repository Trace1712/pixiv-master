from utils.image_data import ImageData
import requests
from bs4 import BeautifulSoup
import json
import utils.utils
import time
import threading


class pixiv():

    def __init__(self, cookie='', thread_number=3):
        self.cookie = cookie
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}
        self.picture_id = []
        self.result = []
        self.thread_number = thread_number

    def set_picture_id(self, id):
        """
        设置图片ID
        param id : 图片ID
        :return
        """
        self.picture_id.append(ImageData(id))

    def get_picture_info(self):
        """
        获取图片 收藏数 浏览量
        :return:
        """
        _count = 0
        while len(self.picture_id) > 0:
            # 获取网页代码
            data = self.picture_id.pop()
            image_data = data.get_info()
            pid = image_data['pid']
            url = "https://www.pixiv.net/artworks/" + pid
            req = requests.get(url, headers=self.headers,
                               cookies=self.cookie).text
            bs = BeautifulSoup(req, 'lxml')
            # 解析html
            for meta in bs.find_all("meta"):
                if len(meta['content']) > 0 and meta['content'][0] == "{":
                    # 处理json数据
                    meta = eval(
                        meta['content'].replace("false", "'false'").replace("null", "'null'").replace("true",
                                                                                                      "'true'"))
                    if 'illust' in meta:
                        # 判断图片是否满足点赞数量的条件
                        if meta['illust'][pid]["likeCount"] >= self.star_number:
                            data.set_info(meta['illust'][pid]['urls']['original'], meta['illust'][pid]["title"],
                                          meta['illust'][pid]["userName"], meta['illust'][pid]["likeCount"], )

                            # 保存图片信息
                            self.result.append(data)
                            _count += 1
        print(threading.current_thread().getName() +
              "共筛选出图片" + str(_count) + "张")

    def download(self):
        """
        下载图片
        :param line_number: 线程名
        :return:
        """
        _count = 0
        while len(self.result) > 0:
            image_data = self.result.pop()
            image = image_data.get_info()
            utils.utils.download_picture(image['url'][0], image['pid'])
            _count += 1
        print(threading.current_thread().getName() +
              "下载完成，共下载图片" + str(_count) + "张")
