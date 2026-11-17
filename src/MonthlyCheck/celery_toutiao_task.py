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


class TouTiaoTask():
    keywords = ["赛乐赛","赛乐赛减肥产品靠谱吗？","赛乐赛减肥产品是真的吗？"]
    keyword_index = 0
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword = None
    page_count = 2
    page_index = 0
    def getMsg(self, msg, count):
        return "头条爬虫：" + msg + ",条数:" + str(count)

    def toutiao(self, keywork, page, brand,  page_count):
        try:
            header = Config.toutiao_header
            param = {
                "keyword": keywork,
                "source": "input",
                "pd": "synthesis",
                "action_type": "pagination",
                "page_num": page,
                # "search_id":"202305171644595FB3718C81D58F825D23",
                "from": "search_tab",
                "cur_tab_title": "search_tab",
                "dvpf": "pc"
            }
            # response1 = proxy.getProxie()
            # print(response1)
            # self.proxles['http'] = 'http://' + response1
            # self.proxles['https'] = 'http://' + response1
            # print(self.proxles)
            url = 'https://so.toutiao.com/search/?' + urlencode(param)
            print(url)
            response = requests.get(url, headers=header)
            print(response.text)
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find_all('script', type="application/json")
            print(len(data))
            array = []
            if len(data) > 6:
                for i in data:
                    # try:
                    t = json.loads(i.string)
                    if "rawData" in t:
                        rawData = t['rawData']
                        if "data" in rawData:
                            data = rawData['data']
                            for item in data:
                                if "merge_article" in item:
                                    merge_article = item['merge_article']
                                    for merge_item in merge_article:
                                        data = {}
                                        url = merge_item['article_url']
                                        data["url"] = url
                                        title = merge_item['title']
                                        data['title'] = title
                                        content = merge_item['abstract']
                                        data['time'] = merge_item['create_time']
                                        data['content'] = content
                                        data['city'] = "广东"
                                        data['mid'] = merge_item['media_creator_id']
                                        data['platform'] = "头条"
                                        data['keywork'] = keywork
                                        data['user_name'] = merge_item['media_name']
                                        data['taskid'] = "0"
                                        data['itemid'] = "0"
                                        data['brand'] = brand
                                        data['status'] = 0
                                        data['pageIndex'] = str(page + 1)
                                        array.append(data)
                                elif "pop_list" in item:
                                    pop_list = item['pop_list']
                                    for pop_item in pop_list:
                                        data = {}
                                        url = pop_item['share_url']
                                        data["url"] = url
                                        title = pop_item['content']
                                        data['title'] = title
                                        data['time'] = pop_item['create_time']
                                        data['content'] = title
                                        data['city'] = "广东"
                                        data['mid'] = pop_item['id']
                                        data['platform'] = "头条"
                                        data['keywork'] = keywork
                                        data['user_name'] = pop_item['media_name']
                                        data['user_url'] = pop_item['user_id']
                                        data['taskid'] = "0"
                                        data['itemid'] = "0"
                                        data['brand'] = brand
                                        data['status'] = 0
                                        data['pageIndex'] = str(page + 1)
                                        array.append(data)
                                else:
                                    data = {}
                                    url = None
                                    if 'url' in item:
                                        url = item['url']
                                    else:
                                        if 'share_url' in item:
                                            url = item['share_url']
                                    title = ""
                                    if "title" in item:
                                        title = item['title']
                                    else:
                                        if 'content' in item:
                                            title = item['content']
                                    id = ""
                                    if 'id' in item:
                                        id = item['id']
                                    media_name = ""
                                    if 'media_name' in item:
                                        media_name = item['media_name']
                                        print(media_name)
                                    create_time = ""
                                    if 'create_time' in item:
                                        create_time = item['create_time']
                                    user_id = ""
                                    if 'user_id' in item:
                                        user_id = item['user_id']

                                    data["url"] = url
                                    title = title
                                    data['title'] = title
                                    data['time'] = create_time
                                    data['content'] = title
                                    data['city'] = "广东"
                                    data['mid'] = id
                                    data['platform'] = "头条"
                                    data['keywork'] = keywork
                                    data['user_name'] = media_name
                                    data['user_url'] = user_id
                                    data['taskid'] = "0"
                                    data['itemid'] = "0"
                                    data['brand'] = brand
                                    data['status'] = 0
                                    data['pageIndex'] = str(page + 1)
                                    if url is not None:
                                        array.append(data)
                analysis = False
                print(array)
                rt = HttpUtils().sendPost(array, "头条", "/api/postMonthlyArticle", analysis)
                if rt.status_code != 200:
                    msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                                   "key值3": "头条上传数据失败"}, "deviceId": "weeds",
                                "type": "markdown"}
                    respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                    print(respone)
                if page < page_count:
                    self.page_index=self.page_index+1
                else:
                    self.page_index=self.page_count+1
            else:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "头条上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
        except Exception as e:
            print(e)

    def run(self, keywork, page, brand, page_count):
        self.toutiao(keywork, page, brand,  page_count)

    def job(self):
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if self.keyword == None:
                    self.page_index = 0
                    respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=头条")
                    print(respone.text)
                    resultdata = respone.json()
                    if len(resultdata) > 0:
                        self.keyword = resultdata['keywork']
                elif self.page_index > self.page_count:
                    self.page_index = 0
                    self.keyword=None
                    respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=头条")
                    print(respone.text)
                    resultdata = respone.json()
                    if len(resultdata) > 0:
                        self.keyword = resultdata['keywork']
                print(self.page_index)
                if self.keyword != None:
                    self.run(self.keyword, self.page_index, "赛乐赛", self.page_count)
                print("这是一个定时任务,更新时间为:" + current_time)
            except Exception as e:
                print("======================")

        # 每隔5分钟运行一次job函数

    def run0(self):
            schedule.every(6).minutes.do(self.job)

            while True:
                # 等待1秒钟
                time.sleep(1)
                # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
                schedule.run_pending()
tt=TouTiaoTask()
tt.run0()