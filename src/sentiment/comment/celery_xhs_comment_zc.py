import time
import sys
sys.path.append('../../')
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
    requests_index=0
    requests_select=0
    xhs_cookie=[Config.xhs_Cookie,Config.xhs_Cookie2,Config.xhs_Cookie3,Config.xhs_Cookie4,Config.xhs_Cookie5,Config.xhs_Cookie6,Config.xhs_Cookie7,Config.xhs_Cookie8,Config.xhs_Cookie9]
    def getSendData(self, array, platform, analysis,isXhsGrass,videoid):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        dd['isXhsGrass']=isXhsGrass
        dd["videoid"]=videoid
        return dd
    
   

    def getComment(self, noteid, cursor,xsec_token,isXhsGrass):
        # file = open("../../lockip.txt", 'r')  # 打开文件
        # response1 = file.read()  # 写入文本
        # print(response1)
        # self.proxles['http'] = 'http://' + response1.strip()
        # self.proxles['https'] = 'http://' + response1.strip()
        # print(self.proxles)
        # file.close()
        # Cookie = "xhsTrackerId=19006738-4c91-4281-a346-edf7ae248360; xhsTrackerId.sig=3YmOVpBQPq2ONxIoBeTcGKIXImdZDArmvnzeN1ZSH_U; a1=1880d8dadcb1fot94dtq78l77gpfb9k13o7kkvm9750000255820; webId=66550f159c2dd748833a1d07e2098067; gid=yYY8fYf0DfqJyYY8fYf0flh6SDyil9j4f9AWWjWY1WWkUT28iDjTyT888J22YJ88yWj8qjdq; gid.sign=PFahmczy10DzFshn9N9S7/eB9tk=; smidV2=20230516151006036a985c286eded8848bfe9fc1d688b8004ab0452aa28ab20; xsecappid=xhs-pc-web; abRequestId=66550f159c2dd748833a1d07e2098067; webBuild=3.10.6; acw_tc=3ac999ee2c855131be7a09eea339841ddd441d7eeec94641edc53f5ef6faa750; websectiga=8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee; sec_poison_id=97d116f0-6e45-46ed-b95c-431044a92d3e; web_session=040069b0f21337d460de8d502b374b677190ac"
        x_cookie=self.xhs_cookie[self.requests_select]
        if self.requests_index>30:
            if self.requests_select<len(self.xhs_cookie)-1:
                self.requests_select+=1
            else:
                self.requests_select=0
            x_cookie=self.xhs_cookie[self.requests_select]
            self.requests_index=0
        xhs_client = XhsClient(x_cookie)
        respon = xhs_client.get_note_comments(noteid, cursor,xsec_token)
        if "msg" in respon:
            if '登录已过期' in respon['msg']:
                print("更换账号")
                if self.requests_select<len(self.xhs_cookie)-1:
                    self.requests_select+=1
                else:
                    self.requests_select=0
                rt = requests.post("http://webstt.jiangxisls.com/api/postComment",
                               json=self.getSendData([{"msg":"登录过期"}], "小红书", False,isXhsGrass,noteid))
        if "code" in respon:
            if respon['code']==300031:
                print("错误了1111111")
                rt = requests.post("http://webstt.jiangxisls.com/api/postComment",
                               json=self.getSendData([{"msg":"当前笔记暂时无法浏览"}], "小红书", False,isXhsGrass,noteid))
                print(rt.text)
        print(respon)
        has_more = respon['has_more']
        if has_more:
            cursor1 = respon['cursor']
        comments = respon['comments']
        array = []
        if len(comments) > 0:
            for comment in comments:
                jj = {}
                jj['platform'] = "小红书"
                jj['videoid'] = comment['note_id']
                jj['comment_id'] = comment['id']
                jj['nickname'] = comment['user_info']['nickname']
                jj['content'] = comment['content']
                jj['comment_time'] = comment['create_time']
                array.append(jj)
                sub_comments = comment['sub_comments']
                if len(sub_comments) > 0:
                    for sub_comment in sub_comments:
                        jj1 = {}
                        jj1['platform'] = "小红书"
                        jj1['videoid'] = sub_comment['note_id']
                        jj1['comment_id'] = sub_comment['id']
                        jj1['nickname'] = sub_comment['user_info']['nickname']
                        jj1['content'] = sub_comment['content']
                        jj1['comment_time'] = sub_comment['create_time']
                        array.append(jj1)
                res = requests.get("http://webstt.jiangxisls.com/api/get/video/comment?aid=" + jj['comment_id'])
                print(res.json())
                if len(res.json()) > 0:
                    rt = requests.post("http://webstt.jiangxisls.com/api/updateVideoStatus",
                                       json={"videoid": noteid, "status": 2})
                    print(rt)
                    has_more = False
        rt = requests.post("http://webstt.jiangxisls.com/api/updateVideoStatus",
                           json={"videoid": noteid, "status": 1})
        print(rt.text)
        rt = requests.post("http://webstt.jiangxisls.com/api/postComment",
                               json=self.getSendData(array, "小红书", False,isXhsGrass,noteid))
        self.requests_index+=1
        if has_more:
            start_time = time.monotonic()
            time.sleep(500)
            end_time = time.monotonic()
            print("任务执行完毕，用时"+str(end_time - start_time)+ "秒")
            self.getComment(noteid, cursor1,xsec_token)
        else:
            start_time = time.monotonic()
            time.sleep(500)
            end_time = time.monotonic()
            print("任务执行完毕，用时"+str(end_time - start_time)+ "秒")
            self.run()

    def run(self):
        res = requests.get("http://webstt.jiangxisls.com/api/getvideo?platform=小红书")
        data = res.json()
        print(data)
        if len(data) > 0:
            try:
                if 'xsec_token' in data[0]:
                    if data[0]['xsec_token']!=None:
                        rt = requests.post("http://webstt.jiangxisls.com/api/updateVideoStatus",
                           json={"videoid":data[0]['videoid'],"status":1})
                        self.getComment(data[0]['videoid'], "",data[0]['xsec_token'],False)
                else:
                    res = requests.get("http://webstt.jiangxisls.com/api/getXhsWithNoteUrl")
                    data = res.json()[0]
                    print(data)
                    noteUrl=data['noteUrl']
                    vid=noteUrl.replace("https://www.xiaohongshu.com/explore/","").split("?")[0]
                    print(vid)
                    xsec_token=noteUrl.replace("https://www.xiaohongshu.com/explore/","").split("?")[1].replace("xsec_token=","").split("&")[0]
                    print(xsec_token)
                    self.getComment(vid, "",xsec_token,True)
                    print(xsec_token)
                    print("这里采集数据")
            except Exception as e:
                print(e)
                print("错误了")
                time.sleep(500)
                self.run()

# dycomment = XhsComment()
# dycomment.run()
x_cookie=Config.xhs_Cookie8
xhs_client = XhsClient(x_cookie)
respon = xhs_client.get_note_comments("6822e4ef000000002100ce02", "","ABTVX2XaERsU8dJlzoAbZ-xVuuqHSgaL7oPzCKXaoibc8=")
comments = respon['comments']
for comment in comments:
    print(json.dumps(comment))