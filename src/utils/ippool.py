import requests, datetime, time
import threading


# 为了限制真实请求时间或函数执行时间的装饰器
class MyThread(threading.Thread):
    def __init__(self, target, args=()):
        """
        why: 因为threading类没有返回值,因此在此处重新定义MyThread类,使线程拥有返回值
        此方法来源 https://www.cnblogs.com/hujq1029/p/7219163.html?utm_source=itdadao&utm_medium=referral
        """
        super(MyThread, self).__init__()
        self.func = target
        self.args = args

    def run(self):
        # 接受返回值
        self.result = self.func(*self.args)

    def get_result(self):
        # 线程不结束,返回值为None
        try:
            return self.result
        except Exception:
            return None


def limit_decor(limit_time):
    """
    :param limit_time: 设置最大允许执行时长,单位:秒
    :return: 未超时返回被装饰函数返回值,超时则返回 None
    """

    def functions(func):
        # 执行操作
        def run(*params):
            thre_func = MyThread(target=func, args=params)
            # 主线程结束(超出时长),则线程方法结束
            thre_func.setDaemon(True)
            thre_func.start()
            # 计算分段沉睡次数
            sleep_num = int(limit_time // 1)
            sleep_nums = round(limit_time % 1, 1)
            # 多次短暂沉睡并尝试获取返回值
            for i in range(sleep_num):
                time.sleep(1)
                infor = thre_func.get_result()
                if infor:
                    return infor
            time.sleep(sleep_nums)
            # 最终返回值(不论线程是否已结束)
            if thre_func.get_result():
                return thre_func.get_result()
            else:
                return "请求超时"  # 超时返回  可以自定义

        return run

    return functions


def get_ip():
    """
    获取代理IP
    :return:
    """
    flag = 0
    while True:
        url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
        req = requests.get(url)
        if req.status_code == 200:
            flag += 1
            result = test_ip(req.text)
            if result != "请求超时":
                print("获取到可用IP")
                return req.text
            else:
                print("IP无效,重新获取")
        else:
            print("请求IP失败,code为%s" % (str(req.status_code)))
        if flag == 3:
            print("失败次数过多无钱了,请联系客服QAQ")
            break


@limit_decor(10)
def test_ip(proxy):
    try:
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}
        url = 'https://www.pixiv.net/ajax/search/artworks/winter?word=winter&order=date_d&mode=all&p=10& ' \
              's_mode=s_tag&type=all&lang = zh '
        proxies = {
            'http': 'http://' + proxy.strip(),
            # 'https': 'https://' + proxy
        }

        with open("cookies.txt", 'r') as f:
            _cookies = {}
            for row in f.read().split(';'):
                k, v = row.strip().split('=', 1)
                _cookies[k] = v
        req = requests.get(url=url, headers=headers, cookies=_cookies, proxies=proxies, allow_redirects=False).text
        return req
    except:
        return "请求超时"
