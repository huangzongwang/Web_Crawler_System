import sys
sys.path.append('../../')
import time
from datetime import datetime

import schedule

from xhs import FeedType, XhsClient
from utils import Config
import requests
import json
import base64
from xhs import help
import execjs

from utils import Proxie
from utils.HttpUtil import HttpUtils


class xhsTask():
    requests_index=0
    requests_select=0
    xhs_cookie=[Config.xhs_Cookie,Config.xhs_Cookie2,Config.xhs_Cookie3,Config.xhs_Cookie4,Config.xhs_Cookie5,Config.xhs_Cookie6,Config.xhs_Cookie7,Config.xhs_Cookie8,Config.xhs_Cookie9]
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword = None
    page_count = 3
    page_index = 0
    keyword_index = 0
    keyword_list = ["赛乐赛 减肥", "赛乐赛 骗子", "赛乐赛  骗局", "赛乐赛 投诉", "赛乐赛", "赛乐赛 没用 ",
                    "赛乐赛 没效果", "赛乐赛 无效", "赛乐赛 坑", "赛乐赛 客服", "赛乐赛不瘦", "赛乐赛 骗", "赛乐赛 退",
                    "赛乐赛 行不行", "赛乐赛 诈骗", "如何投诉 赛乐赛", "用了赛乐赛 没效果", "赛乐赛 骗了多少人",
                    "赛乐赛 受害者", "赛乐赛 骗局曝光", "曝光 赛乐赛", "赛乐赛的真实面目", "赛乐赛 骗钱",
                    "投诉赛乐赛 退钱", "赛乐赛 退款", "赛乐赛在哪里投诉", "赛乐赛 有用吗", "赛乐赛杀猪盘",
                    "为了给老公 赛乐赛", "赛乐赛 为了给老公 "]
    def getMsg(self, msg, count):
        return "小红书爬虫：" + msg + ",条数:" + str(count)

    def run(self, keywork, page, brand, page_count):
        try:
            print(keywork)
            print(page)
            # self.proxles['http'] = 'http://125.125.234.45:4215'
            # self.proxles['https'] = 'http://125.125.234.45:4215'
            # print(self.proxles)
            x_cookie=self.xhs_cookie[self.requests_select]
            if self.requests_index>30:
                if self.requests_select<len(self.xhs_cookie)-1:
                    self.requests_select+=1
                else:
                    self.requests_select=0
            x_cookie=self.xhs_cookie[self.requests_select]
            self.requests_index=0
            print(x_cookie)
            xhs_client = XhsClient(x_cookie)
            notes = xhs_client.get_note_by_keyword(keywork,page=page+1)
            if "msg" in notes:
                if '登录已过期' in notes['msg']:
                    print("更换账号")
                    if self.requests_select<len(self.xhs_cookie)-1:
                        self.requests_select+=1
                    else:
                        self.requests_select=0
            print(json.dumps(notes))
            array = []
            array_user = []
            for note in notes['items']:
                if "xsec_token" in note:
                    xsec_token=note['xsec_token']
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
                    json1['user_id'] = user['user_id']
                    json1['xsec_token'] = user['xsec_token']
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
                    user_data['xsec_token']=xsec_token

                    user_data['status'] = 0
                    user_data['keywork'] = keywork
                    user_data['brand'] = brand
                    user_data['pageIndex'] = str(page + 1)
                    array_user.append(user_data)
                    array.append(json1)

            analysis = False

            rt=HttpUtils().sendPost(array_user, "小红书", "/api/postArticle", analysis)
            if rt.status_code != 200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "快手上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
            HttpUtils().sendPost(array, "小红书", "/api/postArticleUser", analysis)
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
            respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=%E5%B0%8F%E7%BA%A2%E4%B9%A6")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata[0]['keywork']
        elif self.page_index > self.page_count:
            self.page_index = 0
            self.keyword=None
            respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=%E5%B0%8F%E7%BA%A2%E4%B9%A6")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata[0]['keywork']
        if self.keyword!=None:
            self.run(self.keyword, self.page_index, "赛乐赛", self.page_count)
        print("这是一个定时任务,更新时间为:" + current_time)

        # 每隔5分钟运行一次job函数

    def getIp(self):
        response1 = requests.get(
            "http://webapi.http.zhimacangku.com/getip?neek=f062ae82484923b1&num=1&type=1&time=3&pro=0&city=0&yys=0&port=1&pack=0&ts=0&ys=0&cs=0&lb=1&sb=&pb=4&mr=1&regions="
        )
        print(response1.text)
        if response1.text.__contains__("您的余额不足"):
            print("余额不足")
            return "您的账号余额不足"
        elif response1.text.__contains__("请添加白名单"):
            print("白名单没添加")
            detail = response1.json()['msg']
            detail = detail.replace('请添加白名单', '')
            response1 = requests.get(
                "https://wapi.http.linkudp.com/index/index/save_white?neek=2498044&appkey=1e8adc9c673738d041813e8390534490&white=" + detail.strip(),
            )
            print(response1.text.strip())
            return "白名单失效"
        if response1.text.__contains__("请重新提取"):
            print("余额不足")
            return "您的账号余额不足"
        else:
            self.proxles['http'] = 'http://' + response1.text.strip()
            self.proxles['https'] = 'http://' + response1.text.strip()
    def run1(self):
        schedule.every(5).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()


dy=xhsTask()
dy.run1()
# dy.getIp()
# dy.run("赛乐赛", 0, "赛乐赛", 5)
