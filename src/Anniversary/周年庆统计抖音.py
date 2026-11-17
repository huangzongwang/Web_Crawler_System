import sys
sys.path.append('../')
import json
import time
from datetime import datetime

import schedule
from xhs import FeedType, XhsClient
import requests

from sentiment import aliyun_oss_comment
from utils import Config, PhoneNumber
from utils import Proxie
from utils.HttpUtil import HttpUtils


class XhsInfoTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    oss = aliyun_oss_comment.OssService()

    def getSendData(self, array, platform):
        dd = {}
        dd["platform"] = platform
        dd["data"] = array
        return dd

    def xhsinfo(self):
        # try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0  Safari/537.36",
                "Accept": "text/html,application/xhtml+xml, application/xml;q=0 .9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Connection": "keep-alive",
                # "Accept-Encoding": "gzip, deflate, br",
                # "Host": "www.baidu.com",
                # 需要更换Cookie
                "Cookie": "",
            }
            xhs_client = XhsClient(Config.xhs_Cookie)
            res = requests.get("https://znqcrm.jiangxisls.com/Report/Wapvote2025/get_headquartersvote_list?type=dy")
            jsoc = res.json()['data']
            print(jsoc)
            for i in jsoc:
                generalize_url_dy=i['generalize_url_dy']
                if generalize_url_dy==None:
                    continue
                if "xhslink" in generalize_url_dy:
                    continue    
                print(generalize_url_dy)
                if len(generalize_url_dy)>5:
                    generalize_dy_id=""

                    if generalize_url_dy.__contains__("www.douyin.com/discover"):
                        generalize_dy_id=generalize_url_dy.replace("https://www.douyin.com/discover?modal_id=","")
                    elif generalize_url_dy.__contains__("www.douyin.com/video"):
                        generalize_dy_id=generalize_url_dy.replace("https://www.douyin.com/video/","")
                    else:
                        req = requests.get(generalize_url_dy, headers=headers, allow_redirects=False)
                        print(req.headers.get('Location'))
                        if req.headers.get('Location')!=None:
                            if "note" in req.headers.get('Location').split("/?")[0]:
                                generalize_dy_id=req.headers.get('Location').split("/?")[0].replace("https://www.iesdouyin.com/share/note/", "")
                            else:
                                generalize_dy_id=req.headers.get('Location').split("/?")[0].replace("https://www.iesdouyin.com/share/video/", "")
                    if len(generalize_url_dy)==0:
                        continue
                    videoid=generalize_dy_id
                    print(videoid)
                    res = HttpUtils().sendGet(url="/api/getkeyvideid?videoid=" + videoid)
                    if len(res.json()) == 0:
                        print("-======-----")
                        res = HttpUtils().sendPost1(json={"videoid": videoid, "status": 1, "url": str(i['id'])}, url="/api/postkey")
                        print(res.text)
        # except Exception as e:
        #     print("-------------")

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.xhsinfo()
        print("这是一个定时任务,更新时间为:" + current_time)

        # 每隔5分钟运行一次job函数

    def run(self):
        schedule.every(1).minutes.do(self.job)
        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()

ks = XhsInfoTask()
ks.run()
