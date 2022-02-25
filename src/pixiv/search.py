from pixiv.pixivbase import PixivBase
from thread_factory import ThreadFactory
from utils.download import *
import json
from entity.image_data import ImageData


class PixivSearch(PixivBase):
    all_search = 'https://www.pixiv.net/ajax/search/illustrations/{}?word={}&order=date_d&mode=all&p={' \
                 '}&s_mode=s_tag&type=all&lang=zh'

    illustrate_search = 'https://www.pixiv.net/ajax/search/illustrations/{}?word={}&order=date_d&mode=all' \
                        '&p={}&s_mode=s_tag&type=illust&lang=zh '

    def __init__(self, cookie=None, use_proxy=False, num=50, thread_pool=None, download_num=50):
        """
        根据关键词搜索图片
        :param cookie: cookie
        """
        super().__init__(cookie, use_proxy, thread_pool=thread_pool, download_num=download_num)

        self.type = None

        self.page = None

        self.search = None

        self.urls = []

        self.num = num

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

    def run(self):
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
            req = request(self.headers, self.cookie, url, self.proxy, self.ip)
            # 获取图片数据
            self.info = self.info + eval(replace_data(json.loads(json.dumps(req))))['body']['illust']['data']

            logger.info("get picture success {}".format(url))

            if len(self.info) > self.num:
                break

        self.download_task()
