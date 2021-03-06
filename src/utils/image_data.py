class ImageData():

    def __init__(self, id, url="", title="", user_name="", tags=None):
        if tags is None:
            tags = []
        self.pid = id
        self.url = url,
        self.title = title,
        self.user_name = user_name,
        self.star_number = 0,
        self.tags = tags

    def set_info(self, url, title, user_name, star_number):
        """
        设置图片信息
        :param url: 图片地址
        :param title: 图片名称
        :param user_name: 作者姓名
        :param star_number: 点赞数量
        :return:
        """
        self.url = url,
        self.title = title,
        self.user_name = user_name,
        self.star_number = star_number,

    def get_info(self):
        """
        获取图片信息
        :return:
        """
        return {'pid': self.pid,
                'url': self.url,
                'title': self.title,
                'user_name': self.user_name,
                'star_number': self.star_number
                }
