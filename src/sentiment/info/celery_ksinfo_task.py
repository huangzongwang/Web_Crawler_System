import time

from xhs import FeedType, XhsClient
import requests
from baiduspider import BaiduSpider
from pprint import pprint
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json
import urllib.parse
import json
import base64
from src.utils import PhoneNumber, Config
from src.utils.HttpUtil import HttpUtils


class KsInfoTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'

    def getSendData(self, array, platform):
        dd = {}
        dd["platform"] = platform
        dd["data"] = array
        return dd
    def Ksinfo(self):
        ks_header = Config.ks_header
        res = requests.get("http://localhost:5003/api/getksuser")
        print(res)
        jsoc = res.json()['data'][0]
        file = open("/src/lockip.txt", 'r')  # 打开文件
        response1 = file.read()  # 写入文本
        print(response1)
        self.proxles['http'] = 'http://' + response1.strip()
        self.proxles['https'] = 'http://' + response1.strip()
        print(self.proxles)
        file.close()
        url = "https://www.kuaishou.com/profile/" + jsoc['user_id']
        ks_header['Referer'] = url
        r = requests.post("https://www.kuaishou.com/graphql", json={
            "operationName": "visionProfile", "variables": {"userId": jsoc['user_id']},
            "query": "query visionProfile($userId: String) {\n  visionProfile(userId: $userId) {\n    result\n    hostName\n    userProfile {\n      ownerCount {\n        fan\n        photo\n        follow\n        photo_public\n        __typename\n      }\n      profile {\n        gender\n        user_name\n        user_id\n        headurl\n        user_text\n        user_profile_bg_url\n        __typename\n      }\n      isFollowing\n      __typename\n    }\n    __typename\n  }\n}\n"
        }, headers=ks_header,proxies=self.proxles)
        data = r.json()
        print(data)
        userProfile = data['data']['visionProfile']['userProfile']['profile']
        user_text = userProfile['user_text']
        if user_text == '':
            user_text = "未知"
        phone = PhoneNumber.getphone(user_text)
        wechat = PhoneNumber.getwechat(user_text)
        phone_array = []
        if len(phone) > 0:
            phone = phone[0]
            item3 = {}
            item3['phone'] = phone
            item3['platform'] = "快手"
            item3['mid'] = jsoc['photo_id']
            item3['taskid'] = jsoc['taskid']
            item3['itemid'] = jsoc['itemid']
            phone_array.append(item3)
            type = 0
            if jsoc['taskid'] != 0:
                type = 1

        else:
            phone = "查询不到"
        if wechat is None:
            wechat = "查询不到"
        print(phone)
        print(wechat)
        requests.post('http://localhost:5003/api/update/xhsuser',
                      json=self.getSendData(
                          {"sign": user_text, "user_id": jsoc['user_id'], "phone": phone, "wechat": wechat,
                           "red_id": ""},
                          "小红书"))
        if len(phone_array) > 0:
            requests.post('http://localhost:5003/api/post/phone',
                          json=self.getSendData(phone_array,
                                                "快手"))

    def run(self):
            self.Ksinfo()


kstask=KsInfoTask()
kstask.run()
