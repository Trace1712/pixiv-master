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
        # info
        self.info = []
        # 图片ID
        # self.picture_id = []
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

    def run_get_picture_info_producer(self, cnt):
        """
        获取全部图片URL
        :param cnt: info
        :return:
        """
        producer_run(self.condition, 100, 'producer-{}'.format(cnt["id"]), self.get_picture_info,
                     ImageData(pid=cnt['id'], title=cnt["title"], user_name=cnt["userName"], tags=cnt["tags"]))

    def run_download_picture_consumer(self, image):
        """
        下载图片 消费者
        :param image: 图片信息
        :return:
        """
        consumer_run(self.condition, 'consumer-download-{}'.format(image['pid']), download, image)

    def run(self, thread_pool):
        """
        启动
        :return:
        """
        self.get_urls()
        self.finish = False
        """
        页数请求少，单线程就行
        """
        while len(self.urls) > 0:
            url = self.urls.pop()
            req, ip = request(self.headers, self.cookie, url, self.proxy, self.ip)
            self.ip = ip
            # 处理json数据
            _dict = eval(replace_data(json.loads(json.dumps(req))))
            # 获取图片数据
            self.info = self.info + _dict['body']['illust']['data']
            logger.info("get picture success {}", url)

        for cnt in self.info:
            thread_pool.submit(self.run_get_picture_info_producer, cnt)

        for picture in self.result:
            thread_pool.submit(self.run_download_picture_consumer, picture)


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
