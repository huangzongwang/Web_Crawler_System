import sys
sys.path.append('../../')
import time
from datetime import datetime

import schedule

from xhs import FeedType, XhsClient
from src.utils import Config
import requests
import json
import base64
from xhs import help
import execjs

from src.utils import Proxie
from src.utils.HttpUtil import HttpUtils


class xhsTask():
    keywords = ["赛乐赛奥利司他安全吗？","赛乐赛奥利司他是不是真的？"]
    keyword_index = 0
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword = None
    page_count = 2
    page_index = 0

    def getMsg(self, msg, count):
        return "小红书爬虫：" + msg + ",条数:" + str(count)

    def run(self, keywork, page, brand, page_count):
        try:
            print(keywork)
            print(page)
            # self.proxles['http'] = 'http://125.125.234.45:4215'
            # self.proxles['https'] = 'http://125.125.234.45:4215'
            # print(self.proxles)
            xhs_client = XhsClient(Config.xhs_Cookie9)
            notes = xhs_client.get_note_by_keyword(keywork,page=page+1)
            print(notes)
            array = []
            array_user = []
            for note in notes['items']:
                if "note_card" in note:
                    json1 = {}
                    user_data = {}
                    note_card = note['note_card']
                    user = note_card['user']
                    cover = note_card['cover']
                    display_title = ""
                    if "display_title" in note_card:
                        display_title = note_card['display_title']
                    id = note['id']
                    interact_info = note_card['interact_info']
                    liked_count = interact_info['liked_count']
                    url="https://www.xiaohongshu.com/explore/"+id
                    trace_id=""
                    if "url" in cover:
                        url = cover['url']
                    if "trace_id" in cover:
                        trace_id = cover['trace_id']

                    json1['nickname'] = user['nickname']
                    json1['avatar'] = user['avatar']
                    json1['user_id'] = user['user_id']
                    json1['note_id'] = id
                    json1['brand'] = brand
                    json1['taskid'] = 0
                    json1['itemid'] = 0

                    user_data['title'] = display_title
                    user_data['url'] = url
                    user_data['time'] = "未知"
                    user_data['city'] = "广东"
                    cont = {"liked_count": liked_count, "trace_id": trace_id}
                    user_data['content'] = base64.b64encode(json.dumps(cont, indent=2).encode("utf-8")).decode('utf-8')
                    user_data['mid'] = id
                    user_data['taskid'] = 0
                    user_data['itemid'] = 0

                    user_data['status'] = 0
                    user_data['keywork'] = keywork
                    user_data['brand'] = brand
                    user_data['pageIndex'] = str(page + 1)
                    array_user.append(user_data)
                    array.append(json1)

            analysis = False

            rt=HttpUtils().sendPost(array_user, "小红书", "/api/postMonthlyArticle", analysis)
            if rt.status_code != 200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "快手上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
            # HttpUtils().sendPost(array, "小红书", "/api/postArticleUser", analysis)
            if page < page_count:
                self.page_index = self.page_index + 1
            else:
                self.page_index = self.page_count + 1
        except Exception as e:
             print(e)
             # self.getIp()

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.keyword == None:
            self.page_index = 0
            respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=%E5%B0%8F%E7%BA%A2%E4%B9%A6")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata['keywork']
        elif self.page_index > self.page_count:
            self.page_index = 0
            self.keyword=None
            respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=%E5%B0%8F%E7%BA%A2%E4%B9%A6")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata['keywork']
        if self.keyword!=None:
            self.run(self.keyword, self.page_index, "赛乐赛", self.page_count)
        print("这是一个定时任务,更新时间为:" + current_time)
        # 每隔5分钟运行一次job函数


    def run1(self):
        schedule.every(5).minutes.do(self.job)
        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()


dy=xhsTask()
# dy.getIp()
dy.run1()