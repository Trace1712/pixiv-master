from pixiv.pixiv import pixiv
import threading
import utils.utils
import json
import requests


class pixiv_search(pixiv):

    def __init__(self, cookie='', thread_number=3, search='', page=1, star_number=50):
        """
        根据关键词搜索图片
        :param cookie: cookie
        :thread_number: 线程数(默认为3)
        :param search: 搜索关键字
        :param page: 搜索页码数(默认为1)
        :param star_number: ♥数(默认为50)
        """
        super().__init__(cookie, thread_number)

        self.search = search
        self.page = page
        # 设置抓取的图片须满足的点赞数量
        self.star_number = star_number
        # 网页URL
        self.urls = []

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """
        fmt = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}& s_mode = s_tag & ' \
              'type = all & lang = zh '
        urls = [fmt.format(self.search, self.search, p)
                for p in range(1, self.page+1)]
        self.urls = urls

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        _count = 0
        while len(self.urls) > 0:
            url = self.urls.pop()
            req = requests.get(url, headers=self.headers,
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
            info = _dict['body']['illustManga']['data']

            for cnt in info:
                self.set_picture_id(cnt['id'])
                _count += 1
        print(threading.current_thread().getName() + "共找到图片" + str(_count) + "张")

    def run(self):
        """
        运行搜索功能
        :return:
        """
        self.get_urls()
        # 获取线程
        thread_lst = []

        # 启动多个线程 获取图片ID
        for _ in range(self.thread_number):
            t = utils.utils.create_thread(self.run_get_picture_url)
            thread_lst.append(t)
        # 阻塞线程 等执行完后再去筛选图片
        for thread_ in thread_lst:
            thread_.join()

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
