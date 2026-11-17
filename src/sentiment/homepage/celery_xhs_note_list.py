import time

from apscheduler.schedulers.blocking import BlockingScheduler

from xhs import FeedType, XhsClient
import requests
import json
import base64
from xhs import help
import execjs


class xhsTask:
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'

    def getSendData(self, array, platform, analysis):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        return dd

    def run(self, seid, cursor):
        # req = requests.get("http://39.99.33.175:9896/api/queryxhstask")
        # data = req.json()['data']
        # if len(data) > 0:
        Cookie = "xhsTrackerId=19006738-4c91-4281-a346-edf7ae248360; xhsTrackerId.sig=3YmOVpBQPq2ONxIoBeTcGKIXImdZDArmvnzeN1ZSH_U; a1=1880d8dadcb1fot94dtq78l77gpfb9k13o7kkvm9750000255820; webId=66550f159c2dd748833a1d07e2098067; gid=yYY8fYf0DfqJyYY8fYf0flh6SDyil9j4f9AWWjWY1WWkUT28iDjTyT888J22YJ88yWj8qjdq; gid.sign=PFahmczy10DzFshn9N9S7/eB9tk=; smidV2=20230516151006036a985c286eded8848bfe9fc1d688b8004ab0452aa28ab20; cache_feeds=[]; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=c61f9831-a851-477e-b396-ed5939937db8; webBuild=3.3.5; xsecappid=xhs-pc-web; web_session=040069b0f21337d460dee4e6e0364b90261889"
        xhs_client = XhsClient(Cookie)
        # # print( getip("https://api.gahsd62wangdian516.com"))
        data = xhs_client.get_user_notes(seid, cursor)
        print(data)
        has_more = data['has_more']
        cursor1 = data['cursor']
        notes = data['notes']
        notes_list = []
        for note in notes:
            json_note = {}
            json_note['platform'] = "小红书"
            json_note['title'] = note['display_title']
            json_note['url'] = note['cover']['url']
            json_note['account'] = note['user']['user_id']
            json_note['videoid'] = note['note_id']
            notes_list.append(json_note)
            res = requests.get("http://127.0.0.1:5003/api/get/my/video?aid=" + json_note['videoid'])
            print(res.json())
            if len(res.json()['data']) > 0:
                has_more = False

        rt = requests.post("http://webstt.mingyaohui.net/api/postVideoList",
                           json=self.getSendData(notes_list, "抖音", True))
        print(rt.text)
        if has_more:
            time.sleep(500)
            self.run(seid, cursor1)

    def run1(self):
        print("拉取抖音个人信息,获取抖音视频列表")
        res = requests.get("http://127.0.0.1:5003/api/getaccount?platform=小红书")
        print(res.text)
        data = res.json()['data']
        if len(data) > 0:
            sec_uid = str(data[0]['url']).replace("https://www.xiaohongshu.com/user/profile/", '')
            print(sec_uid)
            self.run(sec_uid, "")

nxhsTask = xhsTask()
nxhsTask.run1()

# if __name__ == '__main__':
#     def food_video():
#         nxhsTask = xhsTask()
#         nxhsTask.run1()
#
#     scheduler = BlockingScheduler()
#     # # #
#     # # # # 添加任务
#     scheduler.add_job(food_video, 'interval', minutes=50)
#
#     scheduler.start()
