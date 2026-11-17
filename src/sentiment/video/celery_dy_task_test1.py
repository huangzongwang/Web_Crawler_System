import json
import re
import subprocess
import time
from datetime import datetime

import execjs

import requests
import schedule

from src.douyin_crawler import DyComment
from src.sentiment import aliyun_oss_comment
from src.utils import Proxie, PhoneNumber, Config
from urllib.parse import urlencode
import urllib.parse

from src.utils.HttpUtil import HttpUtils

import random

class DyTask():
    keywords=["赛乐赛奥利司他可以经常吃吗？","赛乐赛投诉","赛乐赛排油是真的脂肪吗"]
    keyword_index = 0
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword=None
    page_count=2
    page_index=0
    oss = aliyun_oss_comment.OssService()


    def getMsg(self, msg, count):
        return "抖音爬虫：" + msg + ",条数:" + str(count)

    def get_ab(self,url):
        p = subprocess.Popen(['node', './a_bogus', url], stdout=subprocess.PIPE)
        url = p.stdout.read().strip()
        return url


    def get_one_agent(sekf):
        return random.choice(sekf.my_headers)

    def get_ms_token(self, randomlength=107):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str
    def dySreach(self, keywork, page, brand, page_count):
        try:
            if page==0:
                offset=0
            else:
                offset=page*10

            req_url = "https://www.douyin.com/discover?modal_id=7258913772092296485"
            dy_comment = DyComment()
            json1 =dy_comment.get_awery_list(req_url, keywork, offset,0)
            data = json1['data']
            array = []
            array_user = []
            phone_array = []
            print(len(data))
            for i in data:
                respon_data = {}
                user_data = {}
                if "aweme_info" in i:
                    aweme_type = 0
                    if "aweme_type" in i['aweme_info']:
                        aweme_type = i['aweme_info']['aweme_type']
                        if aweme_type == 68:
                            aweme_type = 1
                    aweme_id = ""
                    if "aweme_id" in i['aweme_info']:
                        aweme_id = i['aweme_info']['aweme_id']
                    desc = ""
                    if "desc" in i['aweme_info']:
                        desc = i['aweme_info']['desc']
                    create_time = ""
                    if "create_time" in i['aweme_info']:
                        create_time = i['aweme_info']['create_time']
                    uid = ""
                    short_id = ""
                    nickname = ""
                    signature = ""
                    unique_id = ""
                    enterprise_verify_reason = ""
                    sec_uid = ""
                    avatar_larger = ""
                    following_count = ""
                    follower_count = ""
                    if "author" in i['aweme_info']:
                        author = i['aweme_info']['author']
                        if "uid" in author:
                            uid = author['uid']
                        if "short_id" in author:
                            short_id = author['short_id']
                        if "nickname" in author:
                            nickname = author['nickname']
                        if "signature" in author:
                            signature = author['signature']
                        if "unique_id" in author:
                            unique_id = author['unique_id']
                        if "enterprise_verify_reason" in author:
                            enterprise_verify_reason = author['enterprise_verify_reason']
                        if "sec_uid" in author:
                            sec_uid = author['sec_uid']
                        if "avatar_larger" in author:
                            avatar_larger = author['avatar_larger']['uri']
                        if "following_count" in author:
                            following_count = author['following_count']
                        if "follower_count" in author:
                            follower_count = author['follower_count']
                    signature = signature.rstrip()
                    if signature == '':
                        signature = "未知"
                    phone = PhoneNumber.getphone(signature)
                    wechat = PhoneNumber.getwechat(signature)
                    if len(phone) > 0:
                        phone = phone[0]
                        item5 = {}
                        item5['phone'] = phone
                        item5['platform'] = "抖音"
                        item5['mid'] = aweme_id
                        item5['taskid'] = 0
                        item5['itemid'] = 0
                        phone_array.append(item5)
                    else:
                        phone = "查询不到"
                    if wechat is None:
                        wechat = "查询不到"
                    respon_data["aweme_id"] = aweme_id
                    respon_data["uid"] = uid
                    respon_data["short_id"] = short_id
                    respon_data["nickname"] = nickname
                    respon_data["signature"] = signature
                    respon_data["unique_id"] = unique_id
                    respon_data['phone'] = phone
                    respon_data['wechat'] = wechat
                    respon_data["enterprise_verify_reason"] = enterprise_verify_reason
                    respon_data["sec_uid"] = sec_uid
                    respon_data['brand'] = brand
                    respon_data['pic'] = "https://p3-pc.douyinpic.com/aweme/" + avatar_larger
                    respon_data['following_count'] = following_count
                    respon_data['follower_count'] = follower_count
                    respon_data['taskid'] = 0
                    respon_data['itemid'] = 0
                    image_list_url=""
                    # if aweme_type==1:
                    #     if "images" in i['aweme_info']:
                    #         images = i['aweme_info']['images'][0]['download_url_list']
                    #         self.oss.tqdm_download(aweme_id + "_" + str(0) + ".jpg", images[0])
                    #         url_image = self.oss.pushoss(aweme_id + "_" + str(0) + ".jpg",
                    #                                      aweme_id + "_" + str(0) + ".jpg")
                    #         # index_image = index_image + 1
                    #         image_list_url = image_list_url + url_image + ","
                            # index_image=0
                            # old_url=""
                            # for image99 in images:
                            #     print(image99)
                            #     if image99!=old_url:
                            #         self.oss.tqdm_download(aweme_id +"_"+str(index_image)+ ".jpg", image99)
                            #         url_image = self.oss.pushoss(aweme_id +"_"+str(index_image)+ ".jpg", aweme_id +"_"+str(index_image) + ".jpg")
                            #         print(url_image)
                            #         index_image=index_image+1
                            #         image_list_url=image_list_url+url_image+","
                            #         old_url=image99
                    user_data['status'] = 0
                    user_data['title'] = desc
                    user_data['url'] = "https://www.douyin.com/video/" + aweme_id
                    # timeArray = int(time.localtime(create_time))
                    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    user_data['time'] = create_time
                    user_data['city'] = "广东"
                    user_data['videoType'] = aweme_type
                    user_data['content'] = image_list_url
                    user_data['mid'] = aweme_id
                    user_data['keywork'] = keywork
                    user_data['brand'] = brand
                    user_data['taskid'] = 0
                    user_data['itemid'] = 0
                    user_data['pageIndex'] = str(page + 1)
                    if aweme_type!=101:
                        array_user.append(user_data)
                        array.append(respon_data)

            analysis = False
            print(array_user)
            res=HttpUtils().sendPost(array_user, "抖音", "/api/postMonthlyArticle", analysis=analysis)
            print(res.text)
            if res.status_code != 200:
                msg_data = {"title": "weeds测试1", "content": {"平台": "抖音", "动作": "采集",
                                                               "结果": "抖音上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
            if page < page_count:
                if len(data) > 0:
                    self.page_index = self.page_index + 1
                else:
                    self.page_index = self.page_index
            else:
                self.page_index = self.page_count + 1

        except Exception as e:
            print(f"错误了{e}")

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.keyword==None:
            self.page_index = 0
            respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=抖音")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata[0]['keywork']
        elif self.page_index>self.page_count:
            self.page_index=0
            self.keyword=None
            respone = HttpUtils().sendGet("/api/getMonthlyArticleKeywords?platform=抖音")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata[0]['keywork']
        if self.keyword!=None:
            self.dySreach(self.keyword, self.page_index, "赛乐赛", self.page_count)
        print("这是一个定时任务,更新时间为:" + current_time)

    # 每隔5分钟运行一次job函数


    def run(self):
        schedule.every(6).minutes.do(self.job)
        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()




dy=DyTask()
# dy.getIp()
dy.run()

