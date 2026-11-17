import time
import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


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
        xhs_Cookie1="abRequestId=3d9d6870-e417-5baa-ad55-68396e8bf567; a1=18f51ab0d735h7bpiopjwbvgcqgilwkxvwfevzhvv50000426295; webId=fc09c5721a57f234113c9d26ed179ceb; gid=yYi2y0D8DKhjyYi2y0D8fEuxWq2xWDU3lUVEihhDhkSAkd2831ETCh8884JKJj28qii88iS4; web_session=040069b4370fe59161c6c505b7344b44b3872d; webBuild=4.36.5; xsecappid=xhs-pc-web; unread={%22ub%22:%2266e6fe6c000000000c01ad8c%22%2C%22ue%22:%226704aace000000001902ea29%22%2C%22uc%22:21}; websectiga=f3d8eaee8a8c63016320d94a1bd00562d516a5417bc43a032a80cbf70f07d5c0; acw_tc=0ed4a93c19d89d5e1281096a3b58c22db289d15a82201ab75d5546b2fbfe7d7c; sec_poison_id=631c7a6c-d86f-4b44-8526-c72dcb9aaddd"
        xhs_client = XhsClient(cookie=xhs_Cookie1)
        # # print( getip("https://api.gahsd62wangdian516.com"))
        data = xhs_client.get_user_notes(seid, cursor)
        print(data)
        has_more = data['has_more']
        cursor1 = data['cursor']
        notes = data['notes']
        notes_list = []
        for note in notes:
            json_note = {}
            json_note['display_title'] = note['display_title']
            json_note['url'] = "https://www.xiaohongshu.com/explore/"+note['note_id']
            json_note['user_id'] = note['user']['user_id']
            json_note['nickname'] = note['user']['nickname']
            json_note['note_id'] = note['note_id']
            json_note['avatar'] = note['user']['avatar']
            notes_list.append(json_note)
            
        rt = requests.post("http://39.99.33.175:9896/api/xhslist",
                           json=self.getSendData(notes_list, "小红书", True))
        print(rt.text)
        if has_more:
            time.sleep(30)
            self.run(seid, cursor1)

    def run1(self):
        self.run('64acc885000000002a03651d','')
        # print("拉取抖音个人信息,获取抖音视频列表")
        # req = requests.get("http://39.99.33.175:9896/api/queryxhstask")
        # data = req.json()['data']
        # print(data)
        # if len(data) > 0:
            # sec_uid = str(data[0]['user_id'])
            # print(sec_uid)
            # self.run(sec_uid, "")

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
