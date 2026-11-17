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

from src.utils import Proxie, Config
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json

from src.utils.HttpUtil import HttpUtils


class SouGouTask():
    keywords = ["赛乐赛骗子","赛乐赛减肥效果怎么样?"]
    keyword_index = 0
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword = None
    page_count = 2
    page_index = 0
    def getMsg(self, msg, count):
        return "搜狗爬虫：" + msg + ",条数:" + str(count)

    def sougouSreach(self, keywork, page, brand, page_count):
        try:
            sougou_headers = Config.sougou_headers
            # response1 = proxy.getProxie()
            # print(response1)
            # self.proxles['http'] = 'http://' + response1
            # self.proxles['https'] = 'http://' + response1
            # print(self.proxles)
            param = {
                "query": keywork,
                "page": page,
                "ie": "utf-8"
            }
            url = 'https://www.sogou.com/web?' + urlencode(param)  # + v_keyword + '&pn=' + str(page * 10)
            r = requests.get(url, headers=sougou_headers)
            html = r.text
            print("响应码是:{}".format(r.status_code))
            soup = BeautifulSoup(html, "html.parser")
            result_list = soup.find_all(class_='struct201102')

            array = []
            for v in result_list:
                request_data = {}
                title_data = v.find(class_="vr-title")
                href = title_data.find('a', href=True)['href']
                title = title_data.find('a', href=True).text
                real_title_url = ""
                print(href)
                if href.startswith("http"):
                    r = requests.get(href)
                    real_url = re.findall("URL='(.*?)'", r.text)
                    if len(real_url) > 0:
                        real_title_url = real_url[0]
                else:
                    url = "https://www.sogou.com" + v.find('a', href=True)['href']
                    r = requests.get(url)
                    real_url = re.findall("URL='(.*?)'", r.text)
                    if len(real_url) > 0:
                        real_title_url = real_url[0]
                if len(real_title_url) > 0:
                    request_data['title'] = title
                    request_data['url'] = real_title_url
                starwiki = v.find(class_="star-wiki")
                request_data['content'] = ""
                print(starwiki)
                if starwiki is not None:
                    request_data['content'] = starwiki.text
                fintext = v.find(class_="fz-mid space-txt")
                if fintext is not None:
                    request_data['content'] = fintext.text
                citedata = v.find(class_="cite-date")
                request_data['time'] = ""
                if citedata is not None:
                    print(citedata.text)
                    citedatatime = str(citedata.text)
                    if citedatatime.__len__() > 0:
                        print(citedatatime.__len__())
                        citedatatime = citedatatime.strip()[1:citedatatime.__len__()]
                        try:
                            s_t = time.strptime(citedatatime.replace(" ", ""), "%Y-%m-%d")  # 返回元祖
                            mkt = int(time.mktime(s_t))
                            timeArray = time.localtime(int(mkt))
                            citedatatime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                            print(citedatatime)
                            request_data['time'] = citedatatime
                        except Exception as e:
                            print(e)
                request_data['mid'] = str(int(time.time()))
                request_data['city'] = "广东"
                request_data['platform'] = "搜狗"
                request_data['keywork'] = keywork
                request_data['brand'] = brand
                request_data['taskid'] = "0"
                request_data['itemid'] = "0"
                request_data['pageIndex'] = str(page + 1)
                request_data['status'] = 0
                array.append(request_data)

            analysis = False
            rt=HttpUtils().sendPost(array, "搜狗", "/api/postMonthlyArticle", analysis)
            if rt.status_code != 200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "快手上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
            if page < page_count:
                self.page_index=self.page_index+1
            else:
                self.page_index=self.page_count+1
        except Exception as e:
            print(e)

    def run(self, keywork, page, brand,  page_count):
        self.sougouSreach(keywork, page, brand,  page_count)

    def job(self):
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if self.keyword == None:
                    self.page_index = 0
                    respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=搜狗")
                    print(respone.text)
                    resultdata = respone.json()
                    if len(resultdata) > 0:
                        self.keyword = resultdata['keywork']
                elif self.page_index > self.page_count:
                    self.page_index = 0
                    self.keyword=None
                    respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=搜狗")
                    print(respone.text)
                    resultdata = respone.json()
                    if len(resultdata) > 0:
                        self.keyword = resultdata['keywork']
                print(self.page_index)
                if self.keyword != None:
                    self.run(self.keyword, self.page_index, "赛乐赛", self.page_count)
                print("这是一个定时任务,更新时间为:" + current_time)
            except Exception as e:
                print("=====================")

        # 每隔5分钟运行一次job函数

    def run1(self):
            schedule.every(6).minutes.do(self.job)

            while True:
                # 等待1秒钟
                time.sleep(1)
                # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
                schedule.run_pending()



tt=SouGouTask()
tt.run1()