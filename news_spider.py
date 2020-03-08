# -*- coding:utf-8 -*-
import requests
import re
import json
import time
import os
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Cookie":"_ga=GA1.2.1855430798.1461857641; _octo=GH1.1.783519559.1525492869; __lnkrntdmcvrd=-1; tz=Asia%2FShanghai; _gat=1; logged_in=no; _gh_sess=cnRjcDV0K2NCdzNRMVJXdzVkcWRhZys1cFl4S2JVdnRxNlNXbDkzWkNVTlNWTGFqaUVoNXBrcS9kb0lRZGdLT01yNzVLVkFGaUpVKzFmeWd6Uk9vYUg2d2UyUjc3Tkl2S000WXNDQ2xBYVRUbDRSZ3JsVDBhMDdEYVh2cDVMdlBuakxMQ0svNStKNkpob3JsTk5iM1FvT01YaFhqUUZ0cnBjWlpnVml5WHIwaitMajZuODZ2YWhrUHNtWHhQRjJTSm1ZUkl5U0g0cG84MmpoNGtCdGhsOGFsNkEyakYyYjAxNjBOZzBJUHJ4bmJzb3UvUU9TcmlUeERkbmx5RGpWN3A1S0puUkdoUW1YV3JwTGFxRnhaUGt1TnJPcmhQNkxZT0s4UTRSemN0Y2JhanozR1RGWG1qYy9aSjhWR3J3N0RscGlRZ0o5SWNVRDVCc3dSRWxFSzgxZlRjWURVUVFLSjdXaWkvOVRPMWh6MXpXLzBZa1dOQmtCVi9zRVpCUFdlcncyZ1JtaVhNaHAzcDNXRlVUQjdEZz09LS1PWTM4dTJxRUJJTnpuSjBjb3pyeUJ3PT0%3D--9ffec7341c1a6a4a348b68edfb4e7108efaae5e8"
}


def get_news(url, headers):
    content = ''
    url = url
    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html)
    pattern = re.compile('发布时间：(.*)')
    if('成都' in soup.select('h1')[0].string): return 0
    title = soup.select('h1')[0].string  # 标题
    date = pattern.findall(html)[0]  # 时间
    for i in soup.select('p'):  # 内容
        if (i.string):
            content += (' ' + i.string + '\n')
    news = {'title': title,
            'date': date,
            'content': content}
    res = json.dumps(news)
    with open(str(title)+'.txt', 'w', encoding='utf-8')as f:
        f.write(res)


# get_news('https://lajifenleiapp.com/zixun/D7c', headers)
url = 'https://lajifenleiapp.com/zixun'
html = requests.get(url=url, headers=headers).text
soup = BeautifulSoup(html)
pattern = re.compile('<a href="/zixun(.*?)">')
# 写入文件
# for i in pattern.findall(html):
#     get_news(url + i, headers)
#     time.sleep(3)

# 写进数据库
file_dir = 'C:/Users/summer/PycharmProjects/flask_pro/垃圾分类/资讯'
os.chdir('C:/Users/summer/PycharmProjects/flask_pro/垃圾分类/资讯')
for root, dirs, files in os.walk(file_dir):
    for file in files:
        with open(file, 'r')as f:
            res = json.loads(f.read())
            title = res['title']
            date = res['date']
            content = res['content']
