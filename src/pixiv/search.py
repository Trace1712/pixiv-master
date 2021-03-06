import sys
from pixiv.pixivbase import PixivBase
import threading
from utils.util import create_thread, replace_data, join_thread, download, get_ip,request
from utils.image_data import ImageData
import json
import requests


class PixivSearch(PixivBase):

    def __init__(self, cookie='', thread_number=3, search='', page=1, star_number=50, use_proxy=False):
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
        #
        self.picture_id = []

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

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        _count = 0
        while len(self.urls) > 0:
            url = self.urls.pop()
            req = request(self.headers, self.cookie, url, self.proxy)
            new_data = json.loads(json.dumps(req))
            # 处理json数据
            # 字符串转字典
            _dict = eval(replace_data(new_data))
            # 获取图片数据
            print(_dict)
            info = _dict['body']['illust']['data']

            for cnt in info:
                self.picture_id.append(ImageData(id=cnt['id'],title=cnt["title"],user_name=cnt["userName"],tags=cnt["tags"]))
                _count += 1
        print(threading.current_thread().getName() + "共找到图片" + str(_count) + "张")

    def run(self):
        """
        运行搜索功能
        :return:
        """
        self.get_urls()
        # 获取线程
        thread_lst = []

        # 启动多个线程 获取图片ID
        for _ in range(self.thread_number):
            t = create_thread(self.run_get_picture_url)
            thread_lst.append(t)
        # 阻塞线程 等执行完后再去筛选图片
        join_thread(thread_lst)

        # 获取合适图片用于下载
        for _ in range(self.thread_number * 2):
            t = create_thread(self.get_picture_info, self.picture_id)
        thread_lst.append(t)
        # 阻塞线程 等执行完后再去下载图片
        join_thread(thread_lst)

        # 下载图片
        for _ in range(self.thread_number):
            t = create_thread(download, self.result)
        thread_lst.append(t)
        # 阻塞线程 等执行完
        join_thread(thread_lst)
