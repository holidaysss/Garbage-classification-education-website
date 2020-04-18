import json


f = open('garbage.json', encoding="utf-8")
user_dic = json.load(f)
for i in user_dic:
    if(i['category'] != 16):
        print(i['name'])
        print(i['category'])
