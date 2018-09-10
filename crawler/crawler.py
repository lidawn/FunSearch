#coding:utf-8

import requests
from bs4 import BeautifulSoup as BS
import json
#秀动
#大麦
#豆瓣
#微博

user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
                        AppleWebKit/537.36 (KHTML, like Gecko) 
                        Chrome/46.0.2490.80 
                        Safari/537.36
            '''
headers = {
    'user-Agent':user_agent,
    'connection':'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.showstart.com'
    }

def FetchXD():
    URL = "https://www.showstart.com/event/list?cityId=755&siteId=0&isList=1&pageNo=2"

    rsp = requests.get(URL,headers=headers)
    
    content = BS(rsp.content)
    uli = content.find("ul",class_="g-list-wrap justify MT30")
    item_list = uli.find_all("li")
    item_list_json = []
    for item in item_list:
        ToFile(str(item))
        item_json = {}
        a = item.a
        if a != None:
            item_json['link'] = a.get('href')
            item_json['title'] = a.get('title')
            item_json['img'] = item.find('img').get('original')
            artist = item.find('p',class_="performerName").string
            artist = artist.replace('\t','')
            item_json['artist'] = artist.replace('\n','').encode("utf-8")
            item_json['price'] = item.find('b',class_="col-theme").string
            item_json['time'] = item.find('p',class_="g-time").string.encode("utf-8")
            item_json['place'] = item.find('p',class_="g-place a-link").text
            item_list_json.append(item_json)
    json.dump(item_list_json,open('json.txt','w+'))

def ToFile(data):
    f = open("rsp.txt","a+")
    f.write(data)
    f.close() 

FetchXD()