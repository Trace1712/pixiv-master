from image_data import ImageData
import requests
from bs4 import BeautifulSoup
import json
import _thread

class Pixiv():

    def __init__(self, search, page, thread_number, star_number):
        self.search = search
        self.page = page
        #下载所使用的线程数
        self.thread_number = thread_number
        #设置抓取的图片须满足的点赞数量 
        self.star_number = star_number
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}
        # 网页URL
        self.urls = []
        # 图片信息
        self.picture = []
        # 筛选后的图片信息
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
        urls = [fmt.format(self.search, self.search, p)
                for p in range(1, self.page)]
        if(self.page == 1):
            urls = [fmt.format(self.search, self.search, 1)]
        self.urls = urls

    def run_get_picture_url(self):
        """
        获取全部图片URL
        :return:
        """
        while len(self.urls) > 0:
            url = self.urls.pop()
            req = requests.get(url, headers=self.headers,
                               cookies=self.cookies).text
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
                # url = "https://www.pixiv.net/artworks/87860370"
                self.picture.append(ImageData(cnt['id']))
        print("共找到图片"+str(len(self.picture))+"张")

    def get_picture_info(self):
        """
        获取图片 收藏数 浏览量
        :return:
        """
        while len(self.picture) > 0:
            # 获取网页代码
            data = self.picture.pop()
            pid = data.pid
            url = "https://www.pixiv.net/artworks/" + pid
            req = requests.get(url, headers=self.headers,
                               cookies=self.cookies).text
            bs = BeautifulSoup(req, 'lxml')
            # 解析html
            for meta in bs.find_all("meta"):
                if len(meta['content']) > 0 and meta['content'][0] == "{":
                    # 处理json数据
                    meta = eval(
                        meta['content'].replace("false", "'false'").replace("null", "'null'").replace("true",
                                                                                                      "'true'"))
                    if 'illust' in meta:
                        #判断图片是否满足点赞数量的条件
                        if(meta['illust'][pid]["likeCount"] >= self.star_number):
                            data.set_info(meta['illust'][pid]['urls']['original'], meta['illust'][pid]["title"],
                            meta['illust'][pid]["userName"], meta['illust'][pid]["likeCount"],)
                            self.result.append(data)
        print("其中符合条件的图片"+str(len(self.result))+"张")

    def download(self):
        """
        多线程下载图片
        :return:
        """
        print("开始下载")
        for line_number in range(self.thread_number):
            _thread.start_new_thread(self.download_line,(line_number,))

    def download_line(self,line_number):
        """
        多线程下载图片
        :param line_number: 线程名
        :return:
        """
        print("下载线程"+str(line_number)+"启动")
        while len(self.result) > 0 :
            image_data = self.result.pop()
            image = image_data.get_info()
            self.download_picture(image['url'][0], image['pid'])
        print("线程"+str(line_number)+"下载完毕")

    def download_picture(self, url, pid):
        """
        图片下载器
        :param url: 图片地址
        :param id: 图片ID
        :return:
        """
        name=str(pid) + ".jpg"
        header={'Referer': 'https://www.pixiv.net/'}
        req=requests.get(url, headers=header, stream=True)
        if req.status_code == 200:
            open('picture\\' + name, 'wb').write(req.content)  # 将内容写入图片
        else:
            print(name + "下载失败")
        del req


if __name__ == "__main__":
    spider=Pixiv("冬", 5, 3, 100)
    spider.get_urls()
    spider.run_get_picture_url()
    spider.get_picture_info()
    spider.download()
