import requests
import re
import json
import time
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Cookie":"_ga=GA1.2.1855430798.1461857641; _octo=GH1.1.783519559.1525492869; __lnkrntdmcvrd=-1; tz=Asia%2FShanghai; _gat=1; logged_in=no; _gh_sess=cnRjcDV0K2NCdzNRMVJXdzVkcWRhZys1cFl4S2JVdnRxNlNXbDkzWkNVTlNWTGFqaUVoNXBrcS9kb0lRZGdLT01yNzVLVkFGaUpVKzFmeWd6Uk9vYUg2d2UyUjc3Tkl2S000WXNDQ2xBYVRUbDRSZ3JsVDBhMDdEYVh2cDVMdlBuakxMQ0svNStKNkpob3JsTk5iM1FvT01YaFhqUUZ0cnBjWlpnVml5WHIwaitMajZuODZ2YWhrUHNtWHhQRjJTSm1ZUkl5U0g0cG84MmpoNGtCdGhsOGFsNkEyakYyYjAxNjBOZzBJUHJ4bmJzb3UvUU9TcmlUeERkbmx5RGpWN3A1S0puUkdoUW1YV3JwTGFxRnhaUGt1TnJPcmhQNkxZT0s4UTRSemN0Y2JhanozR1RGWG1qYy9aSjhWR3J3N0RscGlRZ0o5SWNVRDVCc3dSRWxFSzgxZlRjWURVUVFLSjdXaWkvOVRPMWh6MXpXLzBZa1dOQmtCVi9zRVpCUFdlcncyZ1JtaVhNaHAzcDNXRlVUQjdEZz09LS1PWTM4dTJxRUJJTnpuSjBjb3pyeUJ3PT0%3D--9ffec7341c1a6a4a348b68edfb4e7108efaae5e8"
}
url = 'https://search.bilibili.com/all?keyword=%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB&from_source=nav_search_new&order=totalrank&duration=0&tids_1=160&page='

for i in range(10):
    url_1 = url + str(i)
    html = requests.get(url_1, headers).text
    title = re.compile('<a title="(.*?)" href').findall(html)  # 标题
    link = re.compile('<a title=".*?" href="(.*?)"').findall(html)  # 链接
    duration = re.compile('"duration":"(.*?)",').findall(html)  # 时长
    #print(date)
    for i in range(len(title)):
        print(title[i] + ' https:'+link[i] + ' ' + duration[i])
    time.sleep(2)
