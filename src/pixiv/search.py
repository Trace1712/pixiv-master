import sys
from pixivbase import PixivBase
import threading
from download import create_thread, replace_data, join_thread, download, request
from src.entity.image_data import ImageData
import json
import requests

from thread_factory import *


class PixivSearch(PixivBase):

    def __init__(self, cookie='', thread_number=3, search='', page=1, star_number=50, use_proxy=False, threadlocal=None):
        """
        根据关键词搜索图片
        :param cookie: cookie
        :thread_number: 线程数(默认为3)
        :param search: 搜索关键字
        :param page: 搜索页码数(默认为1)
        :param star_number: ♥数(默认为50)
        """
        super().__init__(cookie, thread_number, use_proxy, star_number)

        self.search = search
        self.page = page
        # 设置抓取的图片须满足的点赞数量
        self.star_number = star_number
        # 网页URL
        self.urls = []
        # 图片ID
        self.picture_id = []

        self.condition = threading.Condition()  # 创建条件对象

        self.finish = False

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """
        fmt = 'https://www.pixiv.net/ajax/search/illustrations/{}?word={}&order=date_d&mode=all&p={}& s_mode = s_tag & ' \
              'type = all & lang = zh '
        urls = [fmt.format(self.search, self.search, p)
                for p in range(1, self.page + 1)]
        self.urls = urls

    def run_get_picture_url_producer(self, num):
        """
        获取全部图片URL
        :return:
        """
        while len(self.urls) > 0:
            url = self.urls.pop()
            producer_run(self.condition, 100, '搜索生产者-' + str(num + 1), self.run_get_picture_url, url)

        self.finish = True

    def run_get_picture_url(self, url):
        _count = 0
        req, ip = request(self.headers, self.cookie, url, self.proxy, self.ip)
        self.ip = ip
        new_data = json.loads(json.dumps(req))
        # 处理json数据
        # 字符串转字典
        _dict = eval(replace_data(new_data))
        # 获取图片数据
        # print(_dict)
        info = _dict['body']['illust']['data']

        for cnt in info:
            self.get_picture_info(
                picture_id=ImageData(pid=cnt['id'], title=cnt["title"], user_name=cnt["userName"], tags=cnt["tags"]))
            _count += 1

        print(threading.current_thread().getName() + "共找到图片" + str(_count) + "张")

    def run_get_picture_info_consumer(self, num):
        while True:
            consumer_run(self.condition, '图片下载器-' + str(num + 1), download, self.result)
            if self.finish:
                break

    def set_search(self, key):
        self.search = key

    def run(self,thread_pool):
        """
        运行搜索功能
        :return:
        """
        self.get_urls()
        self.finish = False
        for i in range(0, 2):
            thread_pool.submit(self.run_get_picture_url, i)

        for i in range(0, 4):
            thread_pool.submit(self.run_get_picture_info_consumer, i)



        # # 获取线程
        # thread_lst = []
        #
        # # 启动多个线程 获取图片ID
        # for _ in range(self.thread_number):
        #     t = create_thread(self.run_get_picture_url)
        #     thread_lst.append(t)
        # # 阻塞线程 等执行完后再去筛选图片
        # join_thread(thread_lst)

        # 获取合适图片用于下载
        # for _ in range(self.thread_number * 2):
        #     t = create_thread(self.get_picture_info, self.picture_id)
        # thread_lst.append(t)
        # # 阻塞线程 等执行完后再去下载图片
        # join_thread(thread_lst)

        # # 下载图片
        # for _ in range(self.thread_number):
        #     t = create_thread(download, self.result)
        # thread_lst.append(t)
        # # 阻塞线程 等执行完
        # join_thread(thread_lst)
