import tornado.ioloop
import tornado.web
import json
from pixivService import *


class SearchPicture(tornado.web.RequestHandler):

    def get(self):
        """
        get请求

        :keyword 搜索关键字
        :start_page 起始搜索页码
        :end_page 起始搜索页码
        :start_num 点赞数大于多少
        :type 搜索类型
        """
        # key_word = self.get_argument('key_word')
        # start_page = self.get_argument('start_page')
        # end_page = self.get_argument('end_page')
        # start_page = self.get_argument('start_num')
        # type = self.get_argument('type')
        search("winter", 1, 2, 100, 'illustrate')

    def post(self):
        """
        post请求
        测试接口
        a = 1
        b = 2
        """
        arguments = self.request.arguments
        a = arguments['a']
        b = arguments['b']
        c = int(a[0]) + int(b[0])
        self.write("c=" + str(c))


application = tornado.web.Application([(r"/search_picture", SearchPicture), ])
