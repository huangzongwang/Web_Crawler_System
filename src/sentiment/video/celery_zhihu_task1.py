import time
from datetime import datetime

import requests
import schedule

from nltk.sentiment import SentimentAnalyzer

from src.utils import PhoneNumber
from src.utils.HttpUtil import HttpUtils


class ZhiHuTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword = None
    page_count = 2
    page_index = 0
    keywords = ["赛乐赛减肥产品有效吗？","赛乐赛","赛乐赛奥利司他安全吗？"]
    keyword_index = 0

    def getSendData(self, array, platform, analysis):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        return dd

    def zhihuSreach(self, keywork, page, brand):
        r = requests.get("http://127.0.0.1:4005/api/zhihu?q=" + keywork + "&offset=" + str(page))
        data = r.json()
        array = []
        array_user = []
        phone_array = []
        for i in data:
            json = {}
            user_data = {}
            type = i['type']
            if type != "relevant_query":
                highlight = i['highlight']
                if 'title' in highlight:
                    title = highlight['title']
                    user_data['title'] = title
                object = i['object']
                if 'author' in object:
                    if "id" in object:
                        id = object["id"]
                    elif "video_id" in object:
                        id = object["video_id"]
                    else:
                        id = 0

                    user_data['mid'] = id
                    if "created_time" in object:
                        created_time = object['created_time']
                    elif "last_creation_time" in object:
                        created_time = object['last_creation_time']
                    elif "created_at" in object:
                        created_time = object['created_at']
                    else:
                        created_time = ""
                    user_data['content'] = ''
                    note_id = ''
                    if "question" in object:
                        question = object['question']
                        note_id = question['id']
                    json["note_id"] = note_id
                    timeArray = time.localtime(created_time)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    user_data['time'] = otherStyleTime
                    author = object['author']
                    name = author['name']
                    json['name'] = name
                    user_url = author['url']
                    json['user_url'] = user_url
                    voteup_count = author['voteup_count']
                    json['voteup_count'] = voteup_count
                    follower_count = author['follower_count']
                    json['follower_count'] = follower_count
                    avatar_url = author['avatar_url']
                    json['avatar_url'] = avatar_url
                    headline = author['headline']
                    if headline == '':
                        headline = "未知"
                    phone = PhoneNumber.getphone(headline)
                    wechat = PhoneNumber.getwechat(headline)
                    if len(phone) > 0:
                        phone = phone[0]
                        item5 = {}
                        item5['phone'] = phone
                        item5['platform'] = "抖音"
                        item5['mid'] = id
                        item5['taskid'] = 0
                        item5['itemid'] = 0
                        phone_array.append(item5)
                    else:
                        phone = "查询不到"
                    if wechat is None:
                        wechat = "查询不到"
                    json['phone'] = phone
                    json['wechat'] = wechat
                    json['headline'] = headline
                    gender = author['gender']
                    json['gender'] = gender
                if "description" in object:
                    description = object['description']
                    json['description'] = description
                url=""
                if type == "zvideo":
                    url = object['video_url']
                user_data['url'] = url
                user_data['status'] = 0
                user_data['city'] = "东莞"
                user_data['keywork'] = keywork
                json['brand'] = brand
                json['taskid'] = 0
                json['itemid'] = 0
                user_data['brand'] = brand
                user_data['taskid'] = 0
                user_data['itemid'] = 0
            if 'title' in user_data:
                array_user.append(user_data)
                array.append(json)
        print(array)
        print(array_user)
        analysis = False
        res = HttpUtils().sendPost(array_user, "知乎", "/api/postMonthlyArticle", analysis=analysis)
        if page < self.page_count:
            self.page_index = self.page_index + 1
        else:
            self.page_index = self.page_count + 1

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.keyword==None:
            self.page_index = 0
            respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=知乎")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata[0]['keywork']
        elif self.page_index>self.page_count:
            self.page_index=0
            self.keyword=None
            respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=知乎")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata[0]['keywork']
        if self.keyword!=None:
            self.zhihuSreach(self.keyword, self.page_index, "赛乐赛")
        print("这是一个定时任务,更新时间为:" + current_time)

    # 每隔5分钟运行一次job函数

    def run(self):

        schedule.every(6).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()


zh = ZhiHuTask()
zh.run()
