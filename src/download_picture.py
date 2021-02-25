from pixiv.image_data import ImageData
import requests
from bs4 import BeautifulSoup
import json
from utils.utils import *
import time
import threading


class Pixiv():

    def __init__(self, search, page, star_number):
        """

        :param search: 搜索关键字
        :param page: 搜索页码数
        :param star_number: star数
        """
        self.search = search
        self.page = page
        # 设置抓取的图片须满足的点赞数量
        self.star_number = star_number
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}
        # 网页URL
        self.urls = []
        # 图片URL
        self.picture = []
        # 图片信息
        self.result = []

    @property
    def cookies(self):
        with open("cookies.txt", 'r') as f:
            _cookies = {}
            for row in f.read().split(';'):
                k, v = row.strip().split('=', 1)
                _cookies[k] = v
            return _cookies

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """
        fmt = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}& s_mode = s_tag & ' \
              'type = all & lang = zh '
        urls = [fmt.format(self.search, self.search, p)
                for p in range(1, self.page+1)]
        self.urls = urls

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        _count = 0
        while len(self.urls) > 0:
            url = self.urls.pop()
            req = requests.get(url, headers=self.headers,
                               cookies=self.cookies).text
            new_data = json.loads(json.dumps(req))
            line = new_data
            # 处理json数据
            line = line.replace("false", "'false'")
            line = line.replace("null", "'null'")
            line = line.replace("true", "'true'")
            # 单引号转双引号
            line = line.replace("'", "\"")
            # 字符串转字典
            _dict = eval(line)
            # 获取图片数据
            info = _dict['body']['illustManga']['data']

            for cnt in info:
                self.picture.append(ImageData(cnt['id']))
                _count += 1
        print(threading.current_thread().getName() + "共找到图片" + str(_count) + "张")

    def get_picture_info(self):
        """
        获取图片 收藏数 浏览量
        :return:
        """
        _count = 0
        while len(self.picture) > 0:
            # 获取网页代码
            data = self.picture.pop()
            image_data = data.get_info()
            pid = image_data['pid']
            url = "https://www.pixiv.net/artworks/" + pid
            req = requests.get(url, headers=self.headers,
                               cookies=self.cookies).text
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
                            
                            # download_picture(data['url'][0], data['pid'])
                            # 保存图片信息
                            self.result.append(data)
                            _count += 1
        print(threading.current_thread().getName() + "共筛选出图片" + str(_count) + "张")

    def download(self):
        """
        下载图片
        :param line_number: 线程名
        :return:
        """
        _count = 0
        while len(self.result) > 0 :
            image_data = self.result.pop()
            image = image_data.get_info()
            download_picture(image['url'][0], image['pid'])
            _count += 1
        print(threading.current_thread().getName() + "下载完成，共下载图片" + str(_count) + "张")

if __name__ == "__main__":
    thread_number = 3
    spider = Pixiv(search="冬", page=3, star_number=100)
    spider.get_urls()
    # 获取线程
    thread_lst = []


    start =time.perf_counter()
    # 启动多个线程 获取图片ID
    for _ in range(thread_number):
        t = create_thread(spider.run_get_picture_url)
        thread_lst.append(t)
    # 阻塞线程 等执行完后再去筛选图片
    for thread_ in thread_lst:
        thread_.join()
    end = time.perf_counter()
    print('run_get_picture_url Running time: %s Seconds'%(end-start))    

    start =time.perf_counter()
    # 获取合适图片用于下载
    for _ in range(thread_number*2):
        t = create_thread(spider.get_picture_info)
        thread_lst.append(t)
    # 阻塞线程 等执行完后再去下载图片
    for thread_ in thread_lst:
        thread_.join()
    end = time.perf_counter()
    print('get_picture_info Running time: %s Seconds'%(end-start))

    start =time.perf_counter()
    #下载图片
    for _ in range(thread_number):
        t = create_thread(spider.download)
        thread_lst.append(t)
    # 阻塞线程 等执行完
    for thread_ in thread_lst:
        thread_.join()
    end = time.perf_counter()
    print('download Running time: %s Seconds'%(end-start))

    print("退出主线程")
