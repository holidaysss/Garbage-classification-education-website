import requests
import re


url = 'https://search.bilibili.com/all?keyword=%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB&from_source=nav_search_new'
ct = requests.get(url=url)
print(ct.text)