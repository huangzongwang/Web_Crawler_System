import time
from datetime import datetime

import schedule
from xhs import FeedType, XhsClient
import requests

from src.utils import Config
import db.DBHelper as DBHelper


class xhsTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyworks = ['肚子赘肉', '赘肉', '减大臂', '减胯部']
    keyword = None
    page_count = 4
    page_index = 0
    keyword_index = 0

    def getSendData(self, array, platform, analysis):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        return dd

    def run(self, keywork, page):
        print(keywork)
        print(page)
        xhs_client = XhsClient(Config.xhs_Cookie)
        # # print( getip("https://api.gahsd62wangdian516.com"))
        notes = xhs_client.get_note_by_keyword(keywork, page+1)
        print(notes)
        array = []
        for note in notes['items']:
            if "note_card" in note:
                note_card = note['note_card']
                type = note_card['type']
                if type == 'video':
                    display_title = ""
                    if "display_title" in note_card:
                        display_title = note_card['display_title']
                    sql = "INSERT INTO `sentiment_material` (`mid`, `keywork`, `platform`,`location`,`title`,`status`) VALUES (%s, %s, %s,%s, %s, %s)"
                    values = (note['id'], keywork, '小红书', '', display_title, 0)
                    print(values)
                    DBHelper.insert_db(sql,values)
        if page < self.page_count:
            self.page_index = self.page_index + 1
        else:
            self.page_index = self.page_count + 1

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.keyword == None:
            self.page_index = 0
            if self.keyword_index < len(self.keyworks):
                self.keyword = self.keyworks[self.keyword_index]
                self.keyword_index = self.keyword_index + 1

        elif self.page_index > self.page_count:
            self.page_index = 0
            if self.keyword_index < len(self.keyworks):
                self.keyword = self.keyworks[self.keyword_index]
                self.keyword_index = self.keyword_index + 1
        if self.keyword != None:
            self.run(self.keyword, self.page_index)
        print("这是一个定时任务,更新时间为:" + current_time)

        # 每隔5分钟运行一次job函数

    def run1(self):
        schedule.every(1).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()


xhstask = xhsTask()
xhstask.run1()
