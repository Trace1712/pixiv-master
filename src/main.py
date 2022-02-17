from pixiv.search import PixivSearch
from pixiv.daily import PixivDaily
from concurrent.futures import ThreadPoolExecutor


def cookies():
    with open("pixiv/cookies.txt", 'r') as f:
        _cookies = {}
        for row in f.read().split(';'):
            k, v = row.strip().split('=', 1)
            _cookies[k] = v
        return _cookies


def search(num):
    key = "winter"
    search_spider.set_search(key)
    search_spider.run(threadPool, num)


# def case2():
#     recommend_spider.run()
#
#
def daily(num):
    daily_spider.run(threadPool, num)


if __name__ == "__main__":
    cookie = cookies()
    # 创建共用线程池
    threadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix='search')

    # 搜索图片
    search_spider = PixivSearch(cookie=cookie, page=1, star_number=200, use_proxy=False)
    # 日常爬虫
    daily_spider = PixivDaily(cookie=cookie, use_proxy=False)

    search(3)



    # # 推荐图片
    # recommend_spider = PixivRecommend(cookie=cookie, thread_number=3)
    #

    #
    # threadPool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="pixiv")
    #
    # while True:
    #     print('选择功能')
    #     print('1.搜索图片')
    #     print('2.获取推荐图片')
    #     print('3.获取每日热图')
    #     print('4.退出')
    #
    #     case = input('输入指令')
    #
    #     if case == '4':
    #         print('退出程序')
    #         break
    #
    #     switch = {
    #         '1': case1,
    #         '2': case2,
    #         '3': case3
    #     }
    #
    #     try:
    #         logger.info("User is using function %s" % case)
    #         switch[case](cookie)
    #         logger.info("function %s end" % case)
    #     except KeyError as e:
    #         print('请输入正确的指令')
