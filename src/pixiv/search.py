import sys
from pixivbase import PixivBase
from download import *
import json
from src.entity.image_data import ImageData
from thread_factory import *


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
        # 图片ID
        self.picture_id = []
        # 创建条件对象
        self.condition = threading.Condition()
        # 是否完成任务
        self.finish = False

    def set_search(self, key):
        self.search = key

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
            producer_run(self.condition, 100, 'producer_search-{}'.format(str(num + 1)),
                         self.run_get_picture_url, self.urls.pop())
        self.finish = True

    def run_get_picture_url(self, url):
        _count = 0
        req, ip = request(self.headers, self.cookie, url, self.proxy, self.ip)
        self.ip = ip
        new_data = json.loads(json.dumps(req))
        # 处理json数据
        _dict = eval(replace_data(new_data))
        # 获取图片数据
        info = _dict['body']['illust']['data']

        for cnt in info:
            self.get_picture_info(
                picture_id=ImageData(pid=cnt['id'], title=cnt["title"], user_name=cnt["userName"], tags=cnt["tags"]))
            _count += 1

        logger.info("{} finds {} pictures".format(threading.current_thread().getName(), _count))

    def run_download_picture_consumer(self, num):
        """
        下载图片 消费者
        :param num: 线程号
        :return:
        """
        while True:
            consumer_run(self.condition, 'picture_download-{}'.format(num + 1),  download, self.result)
            if self.finish:
                break

    def run(self, thread_pool):
        """
        启动
        :return:
        """
        self.get_urls()
        self.finish = False
        for i in range(0, 2):
            thread_pool.submit(self.run_get_picture_url_producer, i)

        for i in range(0, 2):
            thread_pool.submit(self.run_download_picture_consumer, i)


if __name__ == '__main__':
    def cookies():
        with open("cookies.txt", 'r') as f:
            _cookies = {}
            for row in f.read().split(';'):
                k, v = row.strip().split('=', 1)
                _cookies[k] = v
            return _cookies
    import requests
    cookies = cookies()
    url = 'https://www.pixiv.net/ajax/search/artworks/winter?word=winter&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh'

    # url = "www.baidu.com"
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36'}
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'https://127.0.0.1:7890'
    }
    req = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, allow_redirects=False)
    print(req.status_code)
