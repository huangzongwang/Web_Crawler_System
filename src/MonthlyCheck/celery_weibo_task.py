import sys
sys.path.append('../../')
import time
from datetime import datetime

import schedule
from xhs import FeedType, XhsClient
import requests
from baiduspider import BaiduSpider
from pprint import pprint
import re

from src.utils import Proxie, PhoneNumber, Config
from urllib.parse import urlencode
import json
import base64
from dateutil import parser

from src.utils.HttpUtil import HttpUtils


class WeiboTask():
    keywords = ["赛乐赛奥利司他是正规的吗？","赛乐赛减肥真能瘦吗？","赛乐赛减肥产品有用吗?"]
    keyword_index = 0
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword = None
    page_count = 2
    page_index = 0
    def getMsg(self, msg, count):
        return "微博爬虫：" + msg + ",条数:" + str(count)

    def weibo(self, keywork, page, brand,  page_count):
        try:
            headers = Config.weibo_headers
            param = {
                "gsid": "_2AuZu49XNpZYuRwtW634xdYUNbl_OmGNd1pcespiwIKl9B9C5DmfTsto9THQXie2Z65cd-EIu7OA1jjkrqt_MQ2VehRJI",
                "uid": "1011977931721",
                "from": "1885396040",
                "wm": "90163_90001",
                "c": "weixinminiprogram",
                "v_f": "1",
                "s": "0ffacae4",
                "lang": "zh_CN",
                "count": "10",
                "containerid": "100103type=1&t=3&q=" + keywork,
                "page": page,
            }
            # response1 = proxy.getProxie()
            # print(response1)
            # self.proxles['http'] = 'http://' + response1
            # self.proxles['https'] = 'http://' + response1
            # print(self.proxles)
            url = "https://api.weibo.cn/2/guest/cardlist?" + urlencode(param)
            print(url)
            r = requests.get(url, headers=headers)
            data = r.json()
            print(r.text)
            cards = data['cards']
            array = []
            array_user = []
            phone_array = []
            for card in cards:
                if "mblog" in card:
                    mblog = card['mblog']
                    json1 = {}
                    user_data = {}
                    comments_count = mblog['comments_count']
                    created_at = mblog['created_at']
                    idstr = mblog['idstr']
                    source = mblog['source']
                    text = mblog['text']
                    user = mblog['user']
                    description = user['description']
                    followers_count_str = user['followers_count_str']
                    followers_count = user['followers_count']
                    location = user['location']
                    name = user['name']
                    userid = user['idstr']

                    profile_image_url = user['profile_image_url']

                    json1['idstr'] = idstr
                    json1['description'] = description
                    if description == '':
                        description = "未知"
                    phone = PhoneNumber.getphone(description)
                    wechat = PhoneNumber.getwechat(description)
                    if len(phone) > 0:
                        phone = phone[0]
                        item5 = {}
                        item5['phone'] = phone
                        item5['platform'] = "微博"
                        item5['mid'] = idstr
                        item5['taskid'] = 0
                        item5['itemid'] = 0
                        phone_array.append(item5)

                    else:
                        phone = "查询不到"
                    if wechat is None:
                        wechat = "查询不到"
                    json1['location'] = location
                    json1['username'] = name
                    json1['phone'] = phone
                    json1['wechat'] = wechat
                    json1['userid'] = userid
                    json1['profile_image_url'] = profile_image_url
                    json1['brand'] = brand
                    if "赛乐赛" in text:
                        array.append(json1)

                    user_data['status'] = 0
                    user_data['title'] = text
                    user_data['url'] = source
                    datetime = parser.parse(created_at)
                    timeArray = time.localtime(int(datetime.timestamp()))
                    user_data['time'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    user_data['city'] = location
                    cont = {"followers_count_str": followers_count_str, "followers_count": followers_count,
                            "username": name, "comments_count": comments_count}
                    user_data['content'] = base64.b64encode(json.dumps(cont, indent=2).encode("utf-8")).decode('utf-8')
                    user_data['mid'] = idstr
                    user_data['keywork'] = keywork
                    user_data['pageIndex'] = str(page + 1)
                    json1['brand'] = brand
                    if "赛乐赛" in text:
                        array_user.append(user_data)

                elif "card_group" in card:
                    card_group = card['card_group']
                    item = card_group[0]
                    if "mblog" in item:
                        mblog = item['mblog']
                        json1 = {}
                        user_data = {}
                        comments_count = mblog['comments_count']
                        created_at = mblog['created_at']
                        idstr = mblog['idstr']
                        source = mblog['source']
                        text = mblog['text']
                        user = mblog['user']
                        description = user['description']
                        followers_count_str = user['followers_count_str']
                        followers_count = user['followers_count']
                        location = user['location']
                        name = user['name']
                        userid = user['idstr']
                        profile_image_url = user['profile_image_url']

                        json1['idstr'] = idstr
                        json1['description'] = description
                        if description == '':
                            description = "未知"
                        phone = PhoneNumber.getphone(description)
                        wechat = PhoneNumber.getwechat(description)
                        if len(phone) > 0:
                            phone = phone[0]
                            item5 = {}
                            item5['phone'] = phone
                            item5['platform'] = "微博"
                            item5['mid'] = idstr
                            item5['taskid'] = 0
                            item5['itemid'] = 0
                            phone_array.append(item5)

                        else:
                            phone = "查询不到"
                        if wechat is None:
                            wechat = "查询不到"
                        json1['location'] = location
                        json1['username'] = name
                        json1['taskid'] = 0
                        json1['itemid'] = 0
                        json1['phone'] = phone
                        json1['userid'] = userid
                        json1['wechat'] = wechat
                        json1['profile_image_url'] = profile_image_url
                        json1['brand'] = brand

                        user_data['status'] = 0
                        user_data['title'] = text
                        user_data['url'] = "https://m.weibo.cn/detail/" + idstr
                        datetime = parser.parse(created_at)
                        timeArray = time.localtime(int(datetime.timestamp()))
                        user_data['time'] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        user_data['city'] = location
                        cont = {"followers_count_str": followers_count_str, "followers_count": followers_count,
                                "username": name, "comments_count": comments_count}
                        user_data['content'] = base64.b64encode(json.dumps(cont, indent=2).encode("utf-8")).decode(
                            'utf-8')
                        user_data['mid'] = idstr
                        user_data['keywork'] = keywork
                        user_data['brand'] = brand
                        user_data['taskid'] = 0
                        user_data['pageIndex'] = str(page + 1)
                        user_data['itemid'] = 0
                        if "赛乐赛" in text:
                            array_user.append(user_data)
                            array.append(json1)

            analysis = False
            rt = HttpUtils().sendPost(array_user, "微博", "/api/postMonthlyArticle", analysis)
            if rt.status_code != 200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "微博上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)

            self.page_index=self.page_count+1
        except Exception as e:
            print(e)

    def run(self, keywork, page, brand, page_count):
        self.weibo(keywork, page, brand,  page_count)

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        respone = HttpUtils().sendGet("/api/getMonthlyConfig")
        resultdata = respone.json()
        if 'data' in resultdata:
            for item in resultdata['data']:
                if item['platform'] == "微博":
                    self.keywords = item['keywords']
        else:
            self.keywords = []
        if len(self.keywords)>0:
            if self.keyword == None:
                self.page_index = 0
                respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=微博")
                print(respone.text)
                resultdata = respone.json()
                if len(resultdata) > 0:
                    self.keyword = resultdata['keywork']
            elif self.page_index > self.page_count:
                self.page_index = 0
                self.keyword=None
                respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=微博")
                print(respone.text)
                resultdata = respone.json()
                if len(resultdata) > 0:
                    self.keyword = resultdata['keywork']
            print(self.page_index)
            if self.keyword != None:
                self.run(self.keyword, self.page_index, "赛乐赛", self.page_count)
        print("这是一个定时任务,更新时间为:" + current_time)

        # 每隔5分钟运行一次job函数

    def run1(self):
            schedule.every(6).minutes.do(self.job)
            while True:
                # 等待1秒钟
                time.sleep(1)
                # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
                schedule.run_pending()

tt=WeiboTask()
tt.run1()