import json
import random
import time
from datetime import datetime

import schedule
from xhs import FeedType, XhsClient
import requests

from src.sentiment import aliyun_oss_comment
from src.utils import Config, PhoneNumber
from src.utils.Proxie import Proxie


class XhsInfoTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    oss = aliyun_oss_comment.OssService()
    index=0
    array=[]

    def getSendData(self, array, platform):
        dd = {}
        dd["platform"] = platform
        dd["data"] = array
        return dd

    def xhsinfo(self,noteid):
        try:
            proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
            proixe = Proxie()
            response1 = proixe.getProxie()
            if response1 is not None:
                proxles['http'] = 'http://' + response1
                proxles['https'] = 'http://' + response1
                random_num = random.randint(0, 1)
                print(random_num)
                if random_num==0:
                    xhs_client = XhsClient(Config.xhs_Cookie, proxies=proxles)
                else:
                    xhs_client = XhsClient(Config.xhs_Cookie1, proxies=proxles)
                t = xhs_client.get_note_by_id(noteid)
                consumer = t['video']['consumer']
                url = "https://sns-video-bd.xhscdn.com/" + consumer['origin_video_key']
                print(url)
                self.oss.tqdm_download(noteid + ".mp4", url)
                self.index += 1
        except Exception as e:
            print(e)

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(len(self.array))
        if self.index< len(self.array):
            print(self.array[self.index])
            self.xhsinfo(self.array[self.index])
        print("这是一个定时任务,更新时间为:" + current_time)

        # 每隔5分钟运行一次job函数

    def run(self):
        with open('../list.txt', 'r') as f:
            content = f.read()
        self.array=content.split("\n")
        print(self.array)
        schedule.every(3).minutes.do(self.job)
        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()

ks = XhsInfoTask()
ks.run()
