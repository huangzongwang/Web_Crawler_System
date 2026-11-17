import sys
sys.path.append('../../')
import time

import requests

from utils import Config


class KsComment:
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}

    def getSendData(self, array, platform, analysis):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        return dd

    def getComment(self, userid, photoId, pcursor,taskid):


        # file = open("../../lockip.txt", 'r')  # 打开文件
        # response1 = file.read()  # 写入文本
        # print(response1)
        # self.proxles['http'] = 'http://' + response1.strip()
        # self.proxles['https'] = 'http://' + response1.strip()
        # print(self.proxles)
        # file.close()
        url = "https://www.kuaishou.com/short-video/" + photoId + "?authorId=" + userid + "&streamSource=find&area=homexxbrilliant"
        # ks_header['Referer'] = url
        r = requests.post("https://www.kuaishou.com/graphql", json=
        {"operationName": "commentListQuery", "variables": {"photoId": photoId, "pcursor": pcursor},
         "query": "query commentListQuery($photoId: String, $pcursor: String) {\n  visionCommentList(photoId: $photoId, pcursor: $pcursor) {\n    commentCount\n    pcursor\n    rootComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      authorLiked\n      subCommentCount\n      subCommentsPcursor\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        likedCount\n        realLikedCount\n        liked\n        status\n        authorLiked\n        replyToUserName\n        replyTo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"},
                          headers=Config.ks_login_header)
        print(r.text)
        data = r.json()['data']
        rootComments = data['visionCommentList']['rootComments']
        array = []
        if len(rootComments) > 0:
            for comment in rootComments:
                jj = {}
                jj['taskId'] = taskid
                jj['commentSort'] = 1
                jj['platform'] = "快手"
                jj['videoid'] = photoId
                jj['comment_id'] = comment['commentId']
                jj['nickname'] = comment['authorName']
                jj['content'] = comment['content']
                jj['comment_time'] = comment['timestamp']
                array.append(jj)
        if len(array):
            rt = requests.post("http://webstt.jiangxisls.com/api/postTaskComment",
                               json=self.getSendData(array, "快手", False))
        time.sleep(500)
        self.run()

    def run(self):
        res = requests.get("http://webstt.jiangxisls.com/api/getCompleteTask?platform=2")
        print(res.text)
        aw = res.json()
        if len(aw) > 0:
            try:
                self.getComment(aw[0]['user_id'], aw[0]['url'], "0",aw[0]['id'])
            except Exception:
                print("错误了")
                time.sleep(500)
                self.run()
        else:
            time.sleep(500)
            self.run()


dycomment = KsComment()
dycomment.run()
# if __name__ == '__main__':
#     def food_video():
#         dycomment = KsComment()
#         dycomment.run()
#
#
#     scheduler = BlockingScheduler()
#     # # #
#     # # # # 添加任务
#     scheduler.add_job(food_video, 'interval', minutes=15)
#
#     scheduler.start()
