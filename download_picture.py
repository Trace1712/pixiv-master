import requests
from bs4 import BeautifulSoup

with open("cookies.txt", 'r') as f:
    _cookies = {}
    for row in f.read().split(';'):
        k, v = row.strip().split('=', 1)
        _cookies[k] = v
headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36'}
url = "https://www.pixiv.net/artworks/36199561"

req = requests.get(url, headers=headers, cookies=_cookies).text
# print(req)
bs = BeautifulSoup(req, 'lxml')
header = {'Referer': 'https://www.pixiv.net/'}
for meta in bs.find_all("meta"):
    if len(meta['content']) > 0 and meta['content'][0] == "{":
        # 处理json数据
        meta = eval(
            meta['content'].replace("false", "'false'").replace("null", "'null'").replace("true",
                                                                                          "'true'"))
        if 'illust' in meta:
            picture_url = meta['illust']["36199561"]["urls"]["regular"]
            r = requests.get(picture_url, headers=header, stream=True)
            print(r.status_code)  # 返回状态码
            if r.status_code == 200:
                open('picture\\1.jpg', 'wb').write(r.content)  # 将内容写入图片
                print("done")
            del r

def download_picture(url,id):
    """
    图片下载器
    :param url: 图片地址
    :param id: 图片ID
    :return:
    """
    name = str(id) + ".jpg"
    header = {'Referer': 'https://www.pixiv.net/'}
    req = requests.get(url, headers=header, stream=True)
    if req.status_code == 200:
        open('picture\\'+name, 'wb').write(req.content)  # 将内容写入图片
        print(name+"下载成功")
    else:
        print(name+"下载失败")
    del req