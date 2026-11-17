import sys
sys.path.append('../../')
from datetime import datetime

import requests
import schedule

from src.utils import Proxie, Config
from urllib.parse import urlencode
import time

from src.utils.HttpUtil import HttpUtils


class BilillTask():
    keywords = ["赛乐赛减肥产品有用吗?","赛乐赛减肥产品是真的吗？","赛乐赛减肥产品靠谱吗？"]
    keyword_index = 0
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword = None
    page_count = 2
    page_index = 0
    def getMsg(self, msg, count):
        return "B站爬虫：" + msg + ",条数:" + str(count)

    def bilibiliSreach(self, keywork, page, brand, page_count):
        try:
            # response1 = proxy.getProxie()
            # print(response1)
            # self.proxles['http'] = 'http://' + response1
            # self.proxles['https'] = 'http://' + response1
            # print(self.proxles)
            param = {
                "page": page,
                "page_size": "42",
                "keyword": keywork
            }
            print(param)
            url = "https://api.bilibili.com/x/web-interface/search/all/v2?" + urlencode(param)
            print(url)
            r = requests.get(url, headers=Config.bilibili_headers)
            html = r.json()
            results = html['data']['result']
            print(len(results))
            array = []
            array_user = []
            for result in results:
                result_type = result["result_type"]
                if result_type == "video":
                    data = result['data']
                    for j in data:
                        json1 = {}
                        user_data = {}
                        pubdate = j['pubdate']
                        author = j['author']
                        mid = j['mid']
                        arcurl = j['arcurl']
                        title = j['title']
                        aid = j['aid']
                        upic = j['upic']
                        typename = j['typename']

                        json1['id'] = aid
                        json1['mid'] = mid
                        json1['author'] = author
                        json1['upic'] = upic
                        json1['typename'] = typename
                        json1['brand'] = brand
                        json1['taskid'] = "0"
                        json1['itemid'] = "0"

                        text = title
                        user_data['status'] = 0
                        user_data['title'] = title
                        user_data['url'] = arcurl
                        timeArray = time.localtime(pubdate)
                        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        user_data['time'] = otherStyleTime
                        user_data['city'] = "广东"
                        user_data['content'] = ""
                        user_data['mid'] = mid
                        user_data['taskid'] = "0"
                        user_data['itemid'] = "0"
                        user_data['keywork'] = keywork
                        user_data['brand'] = brand
                        user_data['pageIndex'] = str(page + 1)
                        if "赛乐赛" in title:
                            array_user.append(user_data)
                            array.append(json1)

            analysis = False
            res=HttpUtils().sendPost(array_user, "B站", "/api/postMonthlyArticle", analysis=analysis)
            if res.status_code!=200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "B上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
            if page < page_count:
                self.page_index=self.page_index+1
            else:
                self.page_index = self.page_count + 1
        except Exception as e:
            print(e)

    def run(self, keywork, page, brand, page_count):
        self.bilibiliSreach(keywork, page, brand, page_count)

    def job(self):
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if self.keyword == None:
                    self.page_index = 0
                    respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=B站")
                    print(respone.text)
                    resultdata = respone.json()
                    if len(resultdata) > 0:
                        self.keyword = resultdata['keywork']
                elif self.page_index > self.page_count:
                    self.page_index = 0
                    self.keyword=None
                    respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=B站")
                    print(respone.text)
                    resultdata = respone.json()
                    if len(resultdata) > 0:
                        self.keyword = resultdata['keywork']
                print(self.page_index)
                if self.keyword != None:
                    self.run(self.keyword, self.page_index, "赛乐赛", self.page_count)
                print("这是一个定时任务,更新时间为:" + current_time)
            except Exception as e:
                print("=================")


        # 每隔5分钟运行一次job函数

    def run1(self):
            schedule.every(6).minutes.do(self.job)

            while True:
                # 等待1秒钟
                time.sleep(1)
                # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
                schedule.run_pending()

bibil=BilillTask()
bibil.run1()