from pixiv.pixiv import pixiv
import threading
import utils.utils
import json
import requests
from bs4 import BeautifulSoup


class pixiv_recommand(pixiv):

    def __init__(self, cookie='', thread_number=3):
        super().__init__(cookie, thread_number)
        self.url = 'https://www.pixiv.net/ajax/top/illust?mode=all&lang=zh'

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        _count = 0
        req = requests.get(self.url, headers=self.headers,
                           cookies=self.cookie).text
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
        info = _dict['body']['page']['recommend']['ids']

        for cnt in info:
            self.set_picture_id(cnt)
            _count += 1


    def get_picture_info(self):
        """
        获取图片 ♥数
        :return:
        """
        _count = 0
        while len(self.picture_id) > 0:
            # 获取网页代码
            data = self.picture_id.pop()
            image_data = data.get_info()
            pid = image_data['pid']
            url = "https://www.pixiv.net/artworks/" + pid
            req = requests.get(url, headers=self.headers,
                               cookies=self.cookie).text
            bs = BeautifulSoup(req, 'lxml')
            # 解析html
            for meta in bs.find_all("meta"):
                if len(meta['content']) > 0 and meta['content'][0] == "{":
                    # 处理json数据
                    meta = eval(
                        meta['content'].replace("false", "'false'").replace("null", "'null'").replace("true",
                                                                                                      "'true'"))
                    if 'illust' in meta:

                        data.set_info(meta['illust'][pid]['urls']['original'], meta['illust'][pid]["title"],
                                      meta['illust'][pid]["userName"], meta['illust'][pid]["likeCount"], )

                        # 保存图片信息
                        self.result.append(data)
                        _count += 1
        print(threading.current_thread().getName() +
              "共找到图片" + str(_count) + "张")

    def run(self):
        """
        运行获取推荐图片功能
        :return:
        """
        print()

        self.run_get_picture_url()
        # 获取线程
        thread_lst = []

        # 启动多个线程 获取图片ID
        # for _ in range(self.thread_number):
        #     t = utils.utils.create_thread(self.run_get_picture_url)
        #     thread_lst.append(t)
        # # 阻塞线程 等执行完后再去筛选图片
        # for thread_ in thread_lst:
        #     thread_.join()

        # 获取合适图片用于下载
        for _ in range(self.thread_number*2):
            t = utils.utils.create_thread(self.get_picture_info)
        thread_lst.append(t)
        # 阻塞线程 等执行完后再去下载图片
        for thread_ in thread_lst:
            thread_.join()

        # 下载图片
        for _ in range(self.thread_number):
            t = utils.utils.create_thread(self.download)
        thread_lst.append(t)
        # 阻塞线程 等执行完
        for thread_ in thread_lst:
            thread_.join()
