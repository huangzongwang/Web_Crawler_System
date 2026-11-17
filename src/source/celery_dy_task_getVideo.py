import os.path
import time
from datetime import datetime

import execjs

import requests
import schedule

from src.douyin_crawler import DyComment
from src.sentiment import aliyun_oss_comment
from src.source.db import DBHelper
from src.utils import Proxie, PhoneNumber, Config
from urllib.parse import urlencode
import urllib.parse

from src.utils.HttpUtil import HttpUtils


class DyTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword=None
    page_count=3
    page_index=0
    oss = aliyun_oss_comment.OssService()

    keyword_index=0
    keyword_list =['大肚腩', '胖子运动', '胖子减肥', '大腿甩一甩']
    def getMsg(self, msg, count):
        return "抖音爬虫：" + msg + ",条数:" + str(count)

    def dySreach(self, keywork, page, brand, page_count):
        try:
            dy_headers =Config.dy_header
            dy_headers['Referer'] = "https://www.douyin.com/search/" + urllib.parse.quote(
                keywork) + "?publish_time=0&sort_type=2&type=general"
            if page==0:
                offset=0
            else:
                offset=page*10
            param = {
                "device_platform": "webapp",
                "aid": 6383,
                "channel": "channel_pc_web",
                "search_channel": "aweme_general",
                # "search_channel": "aweme_video_web",
                "sort_type": 2,
                "publish_time": 0,
                "keyword": keywork,
                "search_source": "normal_search",
                "query_correct_type": 1,
                "from_group_id": "",
                "offset":offset,
                "count": 10,
                "pc_client_type": 1,
                "version_code": 190600,
                "version_name": "19.60",
                "cookie_enabled": "false",
                "screen_width": 1920,
                "screen_height": 1080,
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Chrome",
                "browser_version": "113.0.0.0 ",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "",
                "os_name": "Windows",
                "os_version": 10,
                "cpu_core_num": 4,
                "device_memory": 8,
                "platform": "PC",
                "downlink": 10,
                "effective_type": "4g",
                "round_trip_time": 100,
                "webid": "7224418331088242237",

            }

            req_url = "https://www.douyin.com/discover?modal_id=7258913772092296485"
            dy_comment = DyComment()
            json1 = dy_comment.get_awery_list(req_url, keywork, offset, 0)
            data = json1['data']
            print(len(data))
            for i in data:
                if "aweme_info" in i:
                    aweme_id = i['aweme_info']['aweme_id']
                    if "video" in i['aweme_info']:
                        try:
                            desc = ""
                            if "desc" in i['aweme_info']:
                                desc = i['aweme_info']['desc']
                            if "play_addr" in i['aweme_info']['video']:
                                play_addr = i['aweme_info']['video']['play_addr']['url_list'][0]
                                print(play_addr)
                                if not os.path.exists(aweme_id + ".mp4"):
                                    self.oss.tqdm_download(aweme_id +".mp4", play_addr)

                        except Exception as e:
                            print(f"错误了{e}")
            if page < page_count:
                self.page_index=self.page_index+1
            else:
                self.page_index = self.page_count + 1
        except Exception as e:
            print(f"错误了{e}")

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.keyword==None:
            self.page_index = 0
            data = DBHelper.query_db("select * from sentiment_source_keyword where dy_status=0 limit 1")
            update_sql = "UPDATE sentiment_source_keyword SET dy_status = %s WHERE id = %s"
            self.keyword = data[0][0]
            id = data[0][4]
            values = (1, id)
            DBHelper.insert_db(update_sql, values)
        elif self.page_index>self.page_count:
            self.page_index=0
            self.keyword=None
            data = DBHelper.query_db("select * from sentiment_source_keyword where dy_status=0 limit 1")
            update_sql = "UPDATE sentiment_source_keyword SET dy_status = %s WHERE id = %s"
            self.keyword = data[0][0]
            id = data[0][4]
            values = (1, id)
            DBHelper.insert_db(update_sql, values)
        if self.keyword!=None:
            self.dySreach(self.keyword, self.page_index, "赛乐赛", self.page_count)
        print("这是一个定时任务,更新时间为:" + current_time)

    # 每隔5分钟运行一次job函数


    def run(self):
        schedule.every(1).minutes.do(self.job)
        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()




dy=DyTask()
# dy.getIp()
dy.run()

