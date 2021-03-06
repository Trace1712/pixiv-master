from bs4 import BeautifulSoup
import abc
from utils.util import request
import threading


class PixivBase(abc.ABC):

    def __init__(self, cookie='', thread_number=3, use_proxy=False, start_number=50):
        self.cookie = cookie
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}
        self.picture_id = []
        self.result = []
        self.thread_number = thread_number
        # 是否使用代理IP
        self.proxy = use_proxy
        # ⭐
        self.star_number = start_number

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def get_urls(self):
        pass

    def get_picture_info(self, picture_id):
        """
        picture_id:Image_data类型
        获取图片 收藏数 浏览量
        :return:
        """
        _count = 0
        if len(picture_id) == 0:
            print("图片id列表中无内容\n")
        while len(picture_id) > 0:
            # 获取单张图片ID
            data = picture_id.pop()
            image_data = data.get_info()
            pid = str(image_data['pid'])
            # 获取网址
            url = "https://www.pixiv.net/artworks/" + pid
            req = request(self.headers, self.cookie, url, self.proxy)
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

                            # 保存图片信息
                            self.result.append(data)
                            _count += 1
        print(threading.current_thread().getName() + "共筛选出图片" + str(_count) + "张")
