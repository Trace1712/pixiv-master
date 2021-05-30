import sys
from pixiv.search import PixivSearch
from pixiv.recommand import pixiv_recommand
from pixiv.daily import pixiv_daily
from utils.logger import Logger
from utils.util import create_thread
import schedule
import time
import datetime

logger = Logger("hmk").get_log()


def cookies():
    with open("pixiv/cookies.txt", 'r') as f:
        _cookies = {}
        for row in f.read().split(';'):
            k, v = row.strip().split('=', 1)
            _cookies[k] = v
        return _cookies


def case1(cookie):
    # key = input('输入搜索关键词')
    key = "winter"
    spider = PixivSearch(cookie=cookie, thread_number=1,
                         search=key, page=1, star_number=1, use_proxy=False)
    spider.run()


def case2(cookie):
    spider = pixiv_recommand(cookie=cookie, thread_number=3)
    spider.run()


def case3(cookie):
    spider = pixiv_daily(cookie=cookie, thread_number=1)
    spider.run()


def job4():
    print('Job4:每天下午17:49执行一次，每次执行20秒')
    print('Job4-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(20)
    print('Job4-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def job1():
    print('Job1:每隔10秒执行一次的任务，每次执行2秒')
    print('Job1-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(2)
    print('Job1-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def dingshi():
    schedule.every().day.at('12:00').do(job4)
    # schedule.every(10).seconds.do(job1)
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    cookie = cookies()
    create_thread(dingshi)
    while True:

        print('选择功能')
        print('1.搜索图片')
        print('2.获取推荐图片')
        print('3.获取每日热图')
        print('4.退出')

        case = input('输入指令')

        if case == '4':
            print('退出程序')
            break

        switch = {
            '1': case1,
            '2': case2,
            '3': case3
        }

        try:
            logger.info("User is using function %s" % case)
            switch[case](cookie)
            logger.info("function %s end" % case)
        except KeyError as e:
            print('请输入正确的指令')
