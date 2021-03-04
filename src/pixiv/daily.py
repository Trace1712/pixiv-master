import sys
from pixiv.pixivbase import PixivBase
import threading
from utils.utils import create_thread, join_thread, get_ip, replace_data, download, request
from utils.image_data import ImageData
import json
import requests
from bs4 import BeautifulSoup


class pixiv_daily(PixivBase):

    def __init__(self, cookie=None, thread_number=3, num=49,use_proxy=False,):
        super().__init__(cookie, thread_number,use_proxy=use_proxy,start_number=0)
        if cookie is None:
            self.cookie = {}
        if num < 50:
            self.num = 50
        else:
            self.num = num

        # 网页URL
        self.urls = []

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """

        fmt = 'https://www.pixiv.net/ranking.php?p={}&format=json'
        # urls = [fmt.format(p)
        #         for p in range(1, self.page+1)]
        # self.urls = urls
        self.urls = ["https://www.pixiv.net/ranking.php?mode=daily&content=illust"]
        for i in range(self.num  // 50 ):

            self.urls.append(fmt.format(str(i+1)))

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        _count = 0
        url = self.urls.pop(0)
        req = request(self.headers, self.cookie, url, self.proxy)
        bs = BeautifulSoup(req, 'lxml')
        for meta in bs.find_all("a",attrs={"class":"work _work"}):
            self.picture_id.append("https://www.pixiv.net/" + str(meta["href"]))
            _count += 1
            print(meta["href"])
        while len(self.urls) > 0:
            url = self.urls.pop(0)
            req = request(self.headers, self.cookie, url, self.proxy)
            # 解析html
            new_data = json.loads(json.dumps(req))
            # 处理json数据
            # 字符串转字典
            _dict = eval(replace_data(new_data))['contents']
            for info in _dict:
                print(info["illust_id"])
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


if __name__ == '__main__':
    with open("cookies.txt", 'r') as f:
        _cookies = {}
        for row in f.read().split(';'):
            k, v = row.strip().split('=', 1)
            _cookies[k] = v
    spider = pixiv_daily(cookie=_cookies, thread_number=3, num=51)
    spider.get_urls()
    spider.run_get_picture_url()