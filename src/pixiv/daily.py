from pixiv.pixivbase import PixivBase
from utils.download import *
from entity.image_data import ImageData
import json


class PixivDaily(PixivBase):
    # 每日插画
    daily_illustrate_url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p={}&format=json'

    # 每周插画

    # 每日漫画

    def __init__(self, cookie=None, use_proxy=True, thread_pool=None, download_num=50):
        super().__init__(cookie, use_proxy=use_proxy, thread_pool=thread_pool, download_num=download_num)

        self.type = 'daily_illustrate_url'

        self.num = 50

        self.cookie = {} if not cookie else cookie

        # 网页URL
        self.urls = []

    def set_num(self, num, type):
        """

        :param type:
        :param num: 目标数量
        :return:
        """
        self.num = 50 if num < 50 else num
        self.type = type

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """
        fmt = ""
        if self.type == 'daily_illustrate_url':
            fmt = PixivDaily.daily_illustrate_url

        for i in range(self.num // 50):
            self.urls.append(fmt.format(str(i + 1)))

    def run_get_picture_info_producer(self, thread_factory, cnt):
        """
        获取全部图片URL
        :param thread_factory:
        :param cnt: info
        :return:
        """
        image_data = ImageData(pid=cnt['illust_id'], title=cnt['title'], user_name=cnt['user_name'], tags=cnt['tags'],
                               user_id=cnt['user_id'], width=cnt['width'], height=cnt['height'],
                               create_date=cnt['date'])
        thread_factory.producer_run(100, self.get_picture_info, image_data)

        self.finish.append(True)

    def run(self):
        """
        运行搜索功能
        :return:
        """
        self.get_urls()
        while len(self.urls) > 0:
            url = self.urls.pop()
            req = request(self.headers, self.cookie, url, self.proxy, self.ip)
            # 解析html
            new_data = json.loads(json.dumps(req))
            # 处理json数据
            self.info = self.info + eval(replace_data(new_data))['contents']

            logger.info("get picture success {}".format(url))

            if len(self.info) > self.num:
                break

        self.download_task()
