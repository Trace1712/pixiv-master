from apscheduler.schedulers.blocking import BlockingScheduler

from pixiv.search import PixivSearch
from pixiv.daily import PixivDaily
from pixiv.recommandAndFollow import PixivFollowAndRecommend
from concurrent.futures import ThreadPoolExecutor
from pixivControl import *
from constant.constant import *

global search_spider
global daily_spider
global recommend_spider
global sched


def cookies():
    with open("pixiv/cookies.txt", 'r') as f:
        _cookies = {}
        for row in f.read().split(';'):
            k, v = row.strip().split('=', 1)
            _cookies[k] = v
        return _cookies


if __name__ == "__main__":
    cookie = cookies()
    # 创建共用线程池
    threadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix='pixiv')
    # 初始化定时任务
    # sched = BlockingScheduler()
    # sched.start()
    # 初始化搜索任务
    search_spider = PixivSearch(cookie=cookie, use_proxy=False, thread_pool=threadPool, download_num=download_num)
    # 初始化日常任务
    daily_spider = PixivDaily(cookie=cookie, use_proxy=False, thread_pool=threadPool, download_num=download_num)
    # 初始化推荐任务
    recommend_spider = PixivFollowAndRecommend(cookie=cookie, use_proxy=False, thread_pool=threadPool,
                                               download_num=download_num)

    application.listen(server_port)
    tornado.ioloop.IOLoop.instance().start()

    # recommend()

    # search("winter", 1, 2, 100, 'illustrate')

    # daily()
