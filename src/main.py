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


def search(key_word, star_page, end_page, start_num, type, download_num):
    """
    搜索方法
    :param key_word:    关键字
    :param star_page:   开始页数
    :param end_page:    结束页数
    :param start_num:   收藏数
    :param type:        类型 all 全部 illustrate 插画
    :param download_num:下载图片线程数
    :return:
    """
    # 搜索图片
    search_spider = PixivSearch(cookie=cookie, use_proxy=False)
    search_spider.set_search(key_word, start_page=star_page, end_page=end_page, start_num=start_num, type=type)
    search_spider.run(threadPool, download_num)


# def case2():
#     recommend_spider.run()

def daily(num):
    daily_spider.run(threadPool, num)


if __name__ == "__main__":
    cookie = cookies()
    # 创建共用线程池
    threadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix='search')

    # 日常爬虫
    daily_spider = PixivDaily(cookie=cookie, use_proxy=False)

    search("winter", 1, 2, 100, 'illustrate', 10)



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
