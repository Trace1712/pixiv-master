from pixiv.pixivbase import PixivBase
from utils.download import *
from entity.image_data import ImageData
import json


class PixivFollowAndRecommend(PixivBase):

    def __init__(self, cookie=None, use_proxy=True, thread_pool=None, download_num=50):
        super().__init__(cookie, use_proxy=use_proxy, thread_pool=thread_pool, download_num=download_num)

        self.type = None

        self.url = ''

        self.cookie = {} if not cookie else cookie

        self.num = 50

    def get_urls(self):
        self.url = 'https://www.pixiv.net/ajax/top/illust?mode=all&lang=zh'

    def set_num(self, num, type):
        """

        :param type:
        :param num: 目标数量
        :return:
        """
        self.num = 50 if num < 50 else num
        self.type = type

    def run_get_picture_info_producer(self, thread_factory, cnt):
        """
        获取全部图片URL
        :param thread_factory:
        :param cnt: info
        :return:
        """
        image_data = ImageData(pid=cnt['id'], title=cnt['title'], user_name=cnt['userName'], tags=cnt['tags'],
                               user_id=cnt['userId'], width=cnt['width'], height=cnt['height'],
                               create_date=cnt['createDate'])
        thread_factory.producer_run(100, self.get_picture_info, image_data)

    def run(self):
        """
        运行搜索功能
        :return:
        """
        self.get_urls()
        req = request(self.headers, self.cookie, self.url, self.proxy, self.ip)
        # 解析html
        new_data = json.loads(json.dumps(req))
        # 处理json数据
        self.info = self.info + eval(replace_data(new_data))['body']['thumbnails']['illust']

        logger.info("get picture success {}".format(self.url))
        self.info = self.info[:self.num]
        self.download_task()
