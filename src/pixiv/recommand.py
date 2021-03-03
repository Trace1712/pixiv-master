import sys
from pixiv.pixivbase import *
import threading
from utils.utils import *
import json
import requests
from bs4 import BeautifulSoup


class pixiv_recommand(PixivBase):

    def __init__(self, cookie='', thread_number=3):
        super().__init__(cookie, thread_number)
        self.url = 'https://www.pixiv.net/ajax/top/illust?mode=all&lang=zh'

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        _count = 0
        req = requests.get(self.url, headers=self.headers,
                           cookies=self.cookie).text
        new_data = json.loads(json.dumps(req))
        # 处理json数据
        # 字符串转字典
        _dict = eval(replace_data(new_data))
        # 获取图片数据
        info = _dict['body']['page']['recommend']['ids']

        for cnt in info:
            self.set_picture_id(cnt)
            _count += 1


    def run(self):
        """
        运行获取推荐图片功能
        :return:
        """
        print()

        self.run_get_picture_url()
        # 获取线程
        thread_lst = []

        # 启动多个线程 获取图片ID
        # for _ in range(self.thread_number):
        #     t = utils.utils.create_thread(self.run_get_picture_url)
        #     thread_lst.append(t)
        # # 阻塞线程 等执行完后再去筛选图片
        # for thread_ in thread_lst:
        #     thread_.join()

        # 获取合适图片用于下载
        for _ in range(self.thread_number * 2):
            t = create_thread(self.get_picture_info)
        thread_lst.append(t)
        # 阻塞线程 等执行完后再去下载图片
        for thread_ in thread_lst:
            thread_.join()

        # 下载图片
        for _ in range(self.thread_number):
            t = create_thread(self.download)
        thread_lst.append(t)
        # 阻塞线程 等执行完
        for thread_ in thread_lst:
            thread_.join()
