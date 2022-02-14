from pixiv.search import PixivSearch
from utils.logger import Logger
from concurrent.futures import ThreadPoolExecutor

def cookies():
    with open("pixiv/cookies.txt", 'r') as f:
        _cookies = {}
        for row in f.read().split(';'):
            k, v = row.strip().split('=', 1)
            _cookies[k] = v
        return _cookies


def case1():
    # key = input('输入搜索关键词')
    key = "winter"
    search_spider.set_search(key)
    search_spider.run(threadlocal)


# def case2():
#     recommend_spider.run()
#
#
# def case3():
#     daily_spider.run()


if __name__ == "__main__":
    cookie = cookies()
    threadlocal = ThreadPoolExecutor(max_workers=8, thread_name_prefix='search')

    # 搜索图片
    search_spider = PixivSearch(cookie=cookie, thread_number=1,
                                search="", page=1, star_number=1, use_proxy=False)
    case1()
    # # 推荐图片
    # recommend_spider = PixivRecommend(cookie=cookie, thread_number=3)
    #
    # # 日常爬虫
    # daily_spider = PixivDaily(cookie=cookie, thread_number=1)
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
