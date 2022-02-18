import sys
from pixivbase import PixivBase
from download import *
import json
from src.entity.image_data import ImageData
from thread_factory import *


class PixivSearch(PixivBase):
    all_search = 'https://www.pixiv.net/ajax/search/illustrations/{}?word={}&order=date_d&mode=all&p={' \
                 '}&s_mode=s_tag&type=all&lang=zh'

    illustrate_search = 'https://www.pixiv.net/ajax/search/illustrations/{}?word={}&order=date_d&mode=all' \
                        '&p={}&s_mode=s_tag&type=illust&lang=zh '

    def __init__(self, cookie='', use_proxy=False):
        """
        根据关键词搜索图片
        :param cookie: cookie
        """
        super().__init__(cookie, use_proxy)

        self.type = None

        self.page = None

        self.search = None

        self.urls = []

        self.info = []
        # 任务是否完成
        self.finish = []
        # 图片ID
        # self.picture_id = []

    def set_search(self, key="", start_num=100, start_page=1, end_page=2, type='all'):
        """

        :param start_page: 起始页码数
        :param end_page:   终止页码数
        :param key:       搜索关键字
        :param start_num: ♥数(默认为100)
        :param type:      搜索类型，全部 all, 插画 ilustrate
        :return:
        """
        self.search = "{} {}users入り".format(key, self.star_number)
        self.star_number = start_num
        self.start_page = start_page
        self.end_page = end_page if end_page >= start_page else start_page + 1
        self.type = type

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """
        fmt = PixivSearch.all_search if self.type == 'all' else PixivSearch.illustrate_search

        urls = [fmt.format(self.search, self.search, p)
                for p in range(self.start_page, self.end_page)]
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
        logger.info("get total picture {}".format(len(self.info)))
        # get picture info and start download
        thread_factory = ThreadFactory()
        for cnt in self.info:
            thread_pool.submit(self.run_get_picture_info_producer, thread_factory, cnt)

        for _ in range(num):
            thread_pool.submit(self.run_download_picture_consumer, thread_factory)
