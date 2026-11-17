import sys
sys.path.append('../../../')
import time

import requests

from src.sentiment import aliyun_oss_comment
from src.utils import Config
from src.utils.HttpUtil import HttpUtils
from datetime import datetime

import schedule

class KsVideo:
    oss = aliyun_oss_comment.OssService()
    has_more=0
    index=0
    account_url=""
    account_id=""
    max_cursor=""
    account_data=None

    def getMsg(self, msg, count):
        return "快手主页爬虫：" + msg + ",条数:" + str(count)

    def getVideo(self, userid, pcursor):
        try:
            ks_header = Config.ks_login_header
            url = "https://www.kuaishou.com/profile/" + userid
            ks_header['Referer'] = url
            r = requests.post("https://www.kuaishou.com/rest/v/profile/feed", json={"user_id":userid,"pcursor":pcursor,"page":"profile"},
                              headers=ks_header)
            print(r.text)
            data = r.json()
            self.max_cursor = data['pcursor']
            rootComments = data['feeds']
            array = []
            fans_count=1060
            if len(rootComments) > 0:
                self.has_more=2
                array = []
                for comment in rootComments:
                    json_note = {}
                    photo = comment['photo']
                    photo_id = photo['id']
                    url = "https://www.kuaishou.com/short-video/" + photo_id + "?authorId=" + userid + "&streamSource=find&area=homexxbrilliant"
                    print(url)
                    ks_header['Referer'] = url
                    r1 = requests.post("https://www.kuaishou.com/graphql", json={"operationName":"commentListQuery","variables":{"photoId":photo_id,"pcursor":pcursor},"query":"query commentListQuery($photoId: String, $pcursor: String) {\n  visionCommentList(photoId: $photoId, pcursor: $pcursor) {\n    commentCount\n    commentCountV2\n    pcursor\n    rootCommentsV2 {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      hasSubComments\n      likedCount\n      liked\n      status\n      __typename\n    }\n    pcursorV2\n    rootComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      authorLiked\n      subCommentCount\n      subCommentsPcursor\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        likedCount\n        realLikedCount\n        liked\n        status\n        authorLiked\n        replyToUserName\n        replyTo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"},
                          headers=ks_header)
                    data1 = r1.json()['data']
                    print(data1)
                    commentCount=data1['visionCommentList']['commentCountV2']
                    print(commentCount)
                    upvote_total=photo['likeCount']   
                    comment_total=commentCount
                    release_time=photo['timestamp']
                    collect_total=photo['collectCount']
                    readind=photo['viewCount']
                    share_count=0
                    json_note['platform_id']=4
                    json_note['type']='视频'
                    json_note['uid']=photo_id
                    json_note['url']="https://www.kuaishou.com/short-video/"+photo_id
                    json_note['readind']=readind
                    json_note['upvote_total']=upvote_total
                    json_note['comment_total']=comment_total
                    json_note['release_time']=release_time
                    json_note['collect']=collect_total
                    json_note['transpond']=share_count
                    json_note['account_id']=self.account_id
                    json_note['fans_total']=fans_count
                    json_note['collect_type']=2
                    array.append(json_note)
                    time.sleep(15)
                if len(array)>0:
                    ress=requests.post('https://sucai.jxslsyy.com/api/zccollect/get_collect_data',json=array)
                    print(ress.text)
                    # if "photoH265Url" in photo:
                    #     photo_coverUrl = photo['photoH265Url']
                    #     if len(photo_coverUrl) > 10:
                    #         self.oss.tqdm_download("美女_"+photo_id + ".mp4", photo_coverUrl)
                    #     elif "photoUrl" in photo:
                    #         photo_coverUrl = photo['photoUrl']
                    #         if len(photo_coverUrl) > 10:
                    #             self.oss.tqdm_download("美女_"+photo_id + ".mp4", photo_coverUrl)
                    # elif "photoUrl" in photo:
                    #     photo_coverUrl = photo['photoUrl']
                    #     self.oss.tqdm_download("美女_"+photo_id + ".mp4", photo_coverUrl)
            else:
                self.has_more=0
        except Exception as e:
            print("=-=")

    def run(self):
        if self.index==0:
            res10=requests.post("https://sucai.jxslsyy.com/api/zccollect/account_list",json={"platform":4})   
            print(res10.text)
            self.account_data=res10.json()['data']
        if len(self.account_data)>0:
            if self.has_more==0:
                if self.index<len(self.account_data):
                    self.account_url=self.account_data[self.index]['account_url'].replace('https://www.kuaishou.com/profile/','')
                    self.account_id=self.account_data[self.index]['account_id']
                    print(self.account_url)
                    self.index=self.index+1
                else:
                    exit()
            if len(self.account_url):
                print(self.max_cursor)
                self.getVideo(self.account_url, self.max_cursor)    

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
ks=KsVideo()
ks.run1()