import sys
sys.path.append('../../../')
import re
import time
from urllib.parse import urlencode
from src.sentiment import aliyun_oss_comment

import execjs
import requests

from src.utils import Proxie, Config
from src.utils.HttpUtil import HttpUtils
import copy
from datetime import datetime
import schedule

from src.utils.common_utils import CommonUtils
oss = aliyun_oss_comment.OssService()

class VideoScraccy:
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    common_utils = CommonUtils()
    has_more=0
    index=0
    account_url=""
    account_id=""
    max_cursor=0
    account_data=None
    def getMsg(self, msg, count):
        return "抖音主页爬虫：" + msg + ",条数:" + str(count)

    def run(self, url, page, onsuccess, onfail, onfinsh, index):
        print("拉取抖音个人信息,获取抖音视频列表")
        sec_uid = str(url).replace("https://www.douyin.com/user/", '')
        print(sec_uid)
        self.getuserId(sec_uid, page, onsuccess, onfail, onfinsh, index)

    def getuserId(self, sec_uid,cursor):
        try:
            referer_url = f"https://www.douyin.com/"
            ms_token = self.common_utils.get_ms_token()
            webid = "7457730178169832972"
            comment_lsit_req_url = f"https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={sec_uid}&max_cursor={str(cursor)}&locate_item_id=7543172977815244084&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&from_user_page=1&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&cpu_core_num=20&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=140.0.0.0&browser_online=true&engine_name=Blink&engine_version=140.0.0.0&os_name=Windows&os_version=10&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7506362820818634251"
            # comment_lsit_req_url = f"https://www-hj.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={sec_uid}&max_cursor={cursor}&locate_item_id=7293488207273020709&locate_query=false&show_live_replay_strategy=1&need_time_list=0&time_list_query=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&update_version_code=170400&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=128.0.0.0&browser_online=true&engine_name=Blink&engine_version=128.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid={webid}&msToken={ms_token}"
            comment_list_headers1 = copy.deepcopy(Config.dy_header)
            comment_list_headers1['Referer'] = referer_url
            abogus = self.common_utils.get_abogus(comment_lsit_req_url,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

            url = comment_lsit_req_url + "&a_bogus=" + abogus
            print(abogus)
            r = requests.get(url, headers=comment_list_headers1)
            data = r.json()
            self.has_more = data['has_more']
            self.max_cursor = data['max_cursor']
            aweme_list = data['aweme_list']
            fans_count=178
            array = []
            for aweme in aweme_list:
                json_note = {}
                share_url=aweme['share_url']
                uid=aweme['aweme_id']
                statistics=aweme['statistics']
                upvote_total=statistics['digg_count']   
                comment_total=statistics['comment_count']
                release_time=aweme['create_time']
                collect_total=statistics['collect_count']
                share_count=statistics['share_count']
                json_note['platform_id']=2
                json_note['type']='视频'
                json_note['uid']=uid
                json_note['url']=share_url
                json_note['upvote_total']=upvote_total
                json_note['comment_total']=comment_total
                json_note['release_time']=release_time
                json_note['collect']=collect_total
                json_note['transpond']=share_count
                json_note['account_id']=self.account_id
                json_note['fans_total']=fans_count
                json_note['collect_type']=2
                array.append(json_note)
            if len(array)>0:
                ress=requests.post('https://sucai.jxslsyy.com/api/zccollect/get_collect_data',json=array)
                print(ress.text)
                # video=aweme['video']
                # play_addr=video["play_addr"]
                # url_list=play_addr['url_list'][0]
               
                # json_note = {}
                # json_note['platform'] = "抖音"
                # json_note['title'] = aweme['desc']
                # json_note['url'] = aweme['share_url']
                # json_note['account'] = aweme['author']['uid']
                # json_note['videoid'] = aweme['aweme_id']
                # array.append(json_note)
                # res = HttpUtils().sendGet(url="/api/getkeyvideid?videoid=" + aweme['aweme_id'])
                # print(res.json())
                # if len(res.json()) == 0:
                #     print("-======-----")
                #     res = HttpUtils().sendPost1(json={"videoid": aweme['aweme_id'], "status": 1, "url": aweme['aweme_id']}, url="/api/postkey")
                #     print(res.text)
        except Exception as e:
            print(e)

    def run(self):
        if self.index==0:
            res10=requests.post("https://sucai.jxslsyy.com/api/zccollect/account_list",json={"platform":2})   
            print(res10.text)
            self.account_data=res10.json()['data']
        if len(self.account_data)>0:
            if self.has_more==0:
                if self.index<len(self.account_data):
                    self.account_url=self.account_data[self.index]['account_url'].replace('https://www.douyin.com/user/','').replace('?from_tab_name=main','')
                    self.account_id=self.account_data[self.index]['account_id']
                    print(self.account_url)
                    self.index=self.index+1
                else:
                    exit()
            if len(self.account_url):
                print(self.max_cursor)
                self.getuserId(self.account_url, self.max_cursor)
    
    def job(self):
        # try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("这是一个定时任务,更新时间为:" + current_time)
            self.run()
        # except Exception:
        #     print("错误了")

        # 每隔5分钟运行一次job函数
    def run1(self):
        schedule.every(2).minutes.do(self.job)
        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()

video=VideoScraccy()
video.run1()

