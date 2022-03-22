global sched
global search_spider
global daily_spider
global recommend_spider


def search(key_word, star_page, end_page, start_num, type):
    """
    搜索方法
    :param key_word:    关键字
    :param star_page:   开始页数
    :param end_page:    结束页数
    :param start_num:   收藏数
    :param type:        类型 all 全部 illustrate 插画
    :return:
    """

    search_spider.set_search(key_word, start_page=star_page, end_page=end_page, start_num=start_num, type=type)
    search_spider.run()


# @sched.scheduled_job('interval', seconds=3600, id='recommend')
def recommend():
    """
    获取推荐图片
    :return:
    """
    recommend_spider.run()


# @sched.scheduled_job('interval', seconds=3600, id='daily')
def daily():
    """
    日常任务
    :return:
    """
    daily_spider.run()
