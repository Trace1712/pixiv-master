class ImageData:

    def __init__(self, pid, url="", title="", user_name="", user_id="", description="", width=0, height=0,
                 create_date="", tags=None):
        if tags is None:
            tags = []
        # 图片Id
        self.pid = pid
        # 图片url
        self.url = url
        # 图片名称
        self.title = title
        # 用户昵称
        self.user_name = user_name
        # 喜欢数
        self.star_number = 0
        # 标签
        self.tags = tags
        # 用户id
        self.user_id = user_id
        # 图片描述
        self.description = description
        # 图片宽度
        self.width = width
        # 图片高度
        self.height = height
        # 图片上传日期
        self.createDate = create_date

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
