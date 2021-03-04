from bs4 import BeautifulSoup
import abc
from download import *
import threading


class PixivBase(abc.ABC):

    def __init__(self, cookie='', use_proxy=False, start_number=50):
        self.cookie = cookie
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}
        self.picture_id = []
        self.result = []
        # 是否使用代理IP
        self.proxy = use_proxy
        # ⭐
        self.star_number = start_number
        self.ip = None

        self.finish = []

        self.info = []

    @abc.abstractmethod
    def run(self, thread_pool, num):
        pass

    @abc.abstractmethod
    def get_urls(self):
        pass

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

    def get_picture_info(self, picture_id):
        """
        picture_id:Image_data类型
        获取图片 收藏数 浏览量
        :return:
        """
        # 获取单张图片ID
        pid = str(picture_id.get_info()['pid'])
        # 获取网址
        url = "https://www.pixiv.net/artworks/{}".format(pid)
        req, self.ip = request(self.headers, self.cookie, url, self.proxy, self.ip)
        try:
            bs = BeautifulSoup(req, 'html.parser')
        except Exception as e:
            logger.error(e)
        # 解析html
        for meta in bs.find_all("meta"):
            if len(meta['content']) > 0 and meta['content'][0] == "{":
                # 处理json数据
                meta = eval(replace_data(meta['content']))
                if 'illust' in meta:
                    # 判断图片是否满足点赞数量的条件
                    if meta['illust'][pid]["likeCount"] >= self.star_number:
                        picture_id.set_info(meta['illust'][pid]['urls']['original'], meta['illust'][pid]["title"],
                                            meta['illust'][pid]["userName"], meta['illust'][pid]["likeCount"], )

                        # 保存图片信息
                        self.result.append(picture_id)
                        logger.info("{} got picture {}".format(threading.current_thread().getName(), pid))
