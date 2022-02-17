from pixivbase import PixivBase
import threading
from download import create_thread, join_thread, replace_data, download, request
from src.entity.image_data import ImageData
import json
import requests
from bs4 import BeautifulSoup
import time


class PixivDaily(PixivBase):

    def __init__(self, cookie=None, num=49, use_proxy=True):
        super().__init__(cookie, use_proxy=use_proxy, start_number=0)

        self.cookie = {} if not cookie else cookie
        self.num = 50 if num < 50 else num
        # 网页URL
        self.urls = []
        # 全部url
        self._len = 0

    def set_num(self, num):
        self.num = num

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """

        fmt = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p={}&format=json'
        # urls = [fmt.format(p)
        #         for p in range(1, self.page+1)]
        # self.urls = urls
        self.urls = ["https://www.pixiv.net/ranking.php?mode=daily&content=illust"]
        for i in range(self.num // 50):
            self.urls.append(fmt.format(str(i + 1)))
        self._len = len(self.urls)

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        _count = 0
        # 如果第一条数据还没被取走
        if len(self.urls) == self._len:
            url = self.urls.pop(0)
            req, ip = request(self.headers, self.cookie, url, self.proxy, self.ip)
            self.ip = ip
            bs = BeautifulSoup(req, 'lxml')
            for section in bs.find_all("section"):
                _count += 1
                # print(section.img)
                # pid
                pid = section["data-id"]
                # title
                title = section["data-title"]
                # username
                user_name = section["data-user-name"]
                # tags
                tags = section.img["data-tags"]
                self.picture_id.append(ImageData(pid=pid, title=title, user_name=user_name, tags=tags))

        # 取走就直接第二条
        while len(self.urls) > 0:

            url = self.urls.pop(0)
            req, ip = request(self.headers, self.cookie, url, self.proxy, self.ip)
            self.ip = ip
            # 解析html
            new_data = json.loads(json.dumps(req))
            # 处理json数据
            # 字符串转字典
            _dict = eval(replace_data(new_data))['contents']
            for info in _dict:
                self.picture_id.append(ImageData(info["illust_id"]))
                # print(info["illust_id"])
                _count += 1

        print(threading.current_thread().getName() + "共找到图片" + str(_count) + "张")

    def run(self, threadPool, num):
        """
        运行搜索功能
        :return:
        """
        self.get_urls()


if __name__ == '__main__':
    with open("cookies.txt", 'r') as f:
        _cookies = {}
        for row in f.read().split(';'):
            k, v = row.strip().split('=', 1)
            _cookies[k] = v
    print(_cookies)
    # spider = pixiv_daily(cookie=_cookies, thread_number=1, num=51)
    # # spider.get_urls()
    # # spider.run_get_picture_url()
    # spider.run()

    url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
    cookie = _cookies
    ip = "106.110.131.108:4217"
    proxies = {
        'http': 'http://' + ip,
        # 'https': 'https://' + ip
    }
    req = requests.get(url, cookies=cookie, proxies=proxies, allow_redirects=False).text
