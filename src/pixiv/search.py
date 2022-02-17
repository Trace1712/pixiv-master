import sys
from pixivbase import PixivBase
from download import *
import json
from src.entity.image_data import ImageData
from thread_factory import *


class PixivSearch(PixivBase):

    def __init__(self, cookie='', search='', page=1, star_number=100, use_proxy=False):
        """
        根据关键词搜索图片
        :param cookie: cookie
        :thread_number: 线程数(默认为3)
        :param search: 搜索关键字
        :param page: 搜索页码数(默认为1)
        :param star_number: ♥数(默认为50)
        """
        super().__init__(cookie, use_proxy, star_number)

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
        # 任务是否完成
        self.finish = []

    def set_search(self, key):
        self.search = key

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """
        fmt = 'https://www.pixiv.net/ajax/search/illustrations/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag&' \
              'type=all&lang=zh'
        urls = [fmt.format(self.search, self.search, p)
                for p in range(1, self.page + 1)]
        self.urls = urls

    def run_get_picture_info_producer(self, thread_factory, cnt):
        """
        获取全部图片URL
        :param thread_factory:
        :param cnt: info
        :return:
        """
        thread_factory.producer_run(100, self.get_picture_info,
                                    ImageData(pid=cnt['id'], title=cnt["title"],
                                              user_name=cnt["userName"], tags=cnt["tags"],
                                              user_id=cnt["userId"],
                                              description=cnt["description"],
                                              width=cnt["width"], height=cnt["height"],
                                              create_date=cnt["createDate"]
                                              ))

        self.finish.append(True)

    def run_download_picture_consumer(self, thread_factory):
        """
        下载图片 消费者
        :param thread_factory:
        :return:
        """
        while True:
            if len(self.result) != 0:
                thread_factory.consumer_run(download, self.result.pop())
            # 所有图片下载完成, 且获取图片任务全部完成则退出
            if len(self.result) == 0 and len(self.finish) == len(self.info):
                break

    def run(self, thread_pool, num):
        """
        启动
        :return:
        """
        self.get_urls()
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
            logger.info("get picture success {}".format(url))

        thread_factory = ThreadFactory()
        for cnt in self.info:
            thread_pool.submit(self.run_get_picture_info_producer, thread_factory, cnt)

        for _ in range(num):
            thread_pool.submit(self.run_download_picture_consumer, thread_factory)
