import requests
from bs4 import BeautifulSoup
import json


class Pixiv():

    def __init__(self, search, page):
        self.search = search
        self.page = page
        self.result = set()
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}
        # 网页URL
        self.urls = []
        # 图片URL
        self.picture_urls = []
        # 列表类型
        # 字典{id:id,bookmarkCount:bookmarkCount,likeCount:likeCount,viewCount:viewCount}
        self.result = []

    @property
    def cookies(self):
        with open("cookies.txt", 'r') as f:
            _cookies = {}
            for row in f.read().split(';'):
                k, v = row.strip().split('=', 1)
                _cookies[k] = v
            return _cookies

    def get_urls(self):
        """
        获取所有目标URL
        :return:
        """
        fmt = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}& s_mode = s_tag & ' \
              'type = all & lang = zh '
        urls = [fmt.format(self.search, self.search, p) for p in range(1, self.page)]
        self.urls = urls

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        while len(self.urls) > 0:
            url = self.urls.pop()
            req = requests.get(url, headers=self.headers, cookies=self.cookies).text
            new_data = json.loads(json.dumps(req))
            line = new_data[0]
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
                # url = "https://www.pixiv.net/artworks/87860370"
                self.picture_urls.append(cnt['id'])

    def get_picture_info(self):
        """
        获取图片 收藏数 浏览量
        :return:
        """
        while len(self.urls) > 0:
            if len(self.picture_urls) > 0:
                # 获取网页代码
                id = self.picture_urls.pop()
                url = "https://www.pixiv.net/artworks/" + id
                req = requests.get(url, headers=self.headers, cookies=self.cookies).text
                bs = BeautifulSoup(req, 'lxml')
                # 解析html
                for meta in bs.find_all("meta"):
                    if meta['content'][0] == "{":
                        # 处理json数据
                        meta = eval(
                            meta['content'].replace("false", "'false'").replace("null", "'null'").replace("true",
                                                                                                          "'true'"))
                        if 'illust' in meta:
                            print(meta['illust'][id]["bookmarkCount"])
                            print(meta['illust'][id]["likeCount"])
                            print(meta['illust'][id]["viewCount"])

    def download_picture(url, id):
        """
        图片下载器
        :param url: 图片地址
        :param id: 图片ID
        :return:
        """
        name = str(id) + ".jpg"
        header = {'Referer': 'https://www.pixiv.net/'}
        req = requests.get(url, headers=header, stream=True)
        if req.status_code == 200:
            open('picture\\' + name, 'wb').write(req.content)  # 将内容写入图片
            print(name + "下载成功")
        else:
            print(name + "下载失败")
        del req


if __name__ == "__main__":
    spider = Pixiv("winter", 100)
    spider.get_urls()
    spider.get_picture_info()
