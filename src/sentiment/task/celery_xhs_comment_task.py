import sys
sys.path.append('../../')
import time

from xhs import FeedType, XhsClient
import requests
import json
import base64
from xhs import help
import execjs

from utils import Config


class XhsComment:
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

    def getComment(self, noteid, cursor,tastid):
        file = open("../../lockip.txt", 'r')  # 打开文件
        response1 = file.read()  # 写入文本
        print(response1)
        self.proxles['http'] = 'http://' + response1.strip()
        self.proxles['https'] = 'http://' + response1.strip()
        print(self.proxles)
        file.close()
        # Cookie = "xhsTrackerId=19006738-4c91-4281-a346-edf7ae248360; xhsTrackerId.sig=3YmOVpBQPq2ONxIoBeTcGKIXImdZDArmvnzeN1ZSH_U; a1=1880d8dadcb1fot94dtq78l77gpfb9k13o7kkvm9750000255820; webId=66550f159c2dd748833a1d07e2098067; gid=yYY8fYf0DfqJyYY8fYf0flh6SDyil9j4f9AWWjWY1WWkUT28iDjTyT888J22YJ88yWj8qjdq; gid.sign=PFahmczy10DzFshn9N9S7/eB9tk=; smidV2=20230516151006036a985c286eded8848bfe9fc1d688b8004ab0452aa28ab20; abRequestId=66550f159c2dd748833a1d07e2098067; xsecappid=xhs-pc-web; webBuild=4.6.0; acw_tc=0d3c9f022578ff76793c6d4a2ba3613b373a9dd21ab415d911ead960dd6fe5f1; web_session=040069b0f21337d460dee5d1ce374bcd4270bc; unread={%22ub%22:%2265faa3de0000000012030fbb%22%2C%22ue%22:%2265eacf480000000004002c5a%22%2C%22uc%22:25}; websectiga=cf46039d1971c7b9a650d87269f31ac8fe3bf71d61ebf9d9a0a87efb414b816c; sec_poison_id=c2046bcd-f338-4a1f-a0f1-0be6b834d962"
        # Cookie = "xhsTrackerId=19006738-4c91-4281-a346-edf7ae248360; xhsTrackerId.sig=3YmOVpBQPq2ONxIoBeTcGKIXImdZDArmvnzeN1ZSH_U; a1=1880d8dadcb1fot94dtq78l77gpfb9k13o7kkvm9750000255820; webId=66550f159c2dd748833a1d07e2098067; gid=yYY8fYf0DfqJyYY8fYf0flh6SDyil9j4f9AWWjWY1WWkUT28iDjTyT888J22YJ88yWj8qjdq; gid.sign=PFahmczy10DzFshn9N9S7/eB9tk=; smidV2=20230516151006036a985c286eded8848bfe9fc1d688b8004ab0452aa28ab20; xsecappid=xhs-pc-web; abRequestId=66550f159c2dd748833a1d07e2098067; webBuild=3.10.6; acw_tc=3ac999ee2c855131be7a09eea339841ddd441d7eeec94641edc53f5ef6faa750; websectiga=8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee; sec_poison_id=97d116f0-6e45-46ed-b95c-431044a92d3e; web_session=040069b0f21337d460de8d502b374b677190ac"
        xhs_client = XhsClient(Config.xhs_Cookie)
        respon = xhs_client.get_note_comments(noteid, cursor)
        print(respon)
        has_more = respon['has_more']
        if has_more:
            cursor1 = respon['cursor']
        comments = respon['comments']
        array = []
        if len(comments) > 0:
            for comment in comments:
                jj = {}
                jj['taskId'] = tastid
                jj['commentSort'] = 1
                jj['platform'] = "小红书"
                jj['videoid'] = comment['note_id']
                jj['comment_id'] = comment['id']
                jj['nickname'] = comment['user_info']['nickname']
                jj['content'] = comment['content']
                jj['comment_time'] = comment['create_time']
                array.append(jj)
        if len(array):
            rt = requests.post("http://webstt.jiangxisls.com/api/postTaskComment",
                               json=self.getSendData(array, "抖音", False))

        time.sleep(500)
        self.run()

    def run(self):
        res = requests.get("http://webstt.jiangxisls.com/api/getCompleteTask?platform=3")
        data = res.json()
        print(data)
        if len(data) > 0:
            try:
                self.getComment(data[0]['url'], "",data[0]['id'])
            except Exception:
                print("错误了")
                time.sleep(500)
                self.run()
        else:
            time.sleep(500)
            self.run()

dycomment = XhsComment()
dycomment.run()