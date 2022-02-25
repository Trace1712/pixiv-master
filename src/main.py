from pixiv.search import PixivSearch
from pixiv.daily import PixivDaily
from pixiv.recommandAndFollow import PixivFollowAndRecommend
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
download_num = 5


def cookies():
    with open("pixiv/cookies.txt", 'r') as f:
        _cookies = {}
        for row in f.read().split(';'):
            k, v = row.strip().split('=', 1)
            _cookies[k] = v
        return _cookies


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


@sched.scheduled_job('interval', seconds=3600, id='recommend')
def recommend():
    """
    获取推荐图片
    :return:
    """
    recommend_spider.run()


@sched.scheduled_job('interval', seconds=3600, id='daily')
def daily():
    """
    日常任务
    :return:
    """
    daily_spider.run()


if __name__ == "__main__":
    cookie = cookies()
    # 创建共用线程池
    threadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix='pixiv')
    # 初始化定时任务
    # sched.start()
    # 初始化搜索任务
    search_spider = PixivSearch(cookie=cookie, use_proxy=False, thread_pool=threadPool, download_num=10)
    # 初始化日常任务
    daily_spider = PixivDaily(cookie=cookie, use_proxy=False, thread_pool=threadPool, download_num=10)
    # 初始化推荐任务
    recommend_spider = PixivFollowAndRecommend(cookie=cookie, use_proxy=False, thread_pool=threadPool, download_num=10)
    # recommend()

    search("winter", 1, 2, 100, 'illustrate')
