import time
import sys
sys.path.append('../../')
import requests

from utils import Config


class KsComment:
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}

    def getSendData(self, array, platform, analysis,videoid):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        dd["videoid"]=videoid
        return dd

    def getComment(self, userid, photoId, pcursor):
        ks_header=Config.ks_login_header
        # file = open("../../lockip.txt", 'r')  # 打开文件
        # response1 = file.read()  # 写入文本
        # print(response1)
        # self.proxles['http'] = 'http://' + response1.strip()
        # self.proxles['https'] = 'http://' + response1.strip()
        # print(self.proxles)
        # file.close()
        url = "https://www.kuaishou.com/short-video/" + photoId + "?authorId=" + userid + "&streamSource=find&area=homexxbrilliant"
        print(url)
        ks_header['Referer'] = url
        r = requests.post("https://www.kuaishou.com/graphql", json={"operationName":"commentListQuery","variables":{"photoId":photoId,"pcursor":pcursor},"query":"query commentListQuery($photoId: String, $pcursor: String) {\n  visionCommentList(photoId: $photoId, pcursor: $pcursor) {\n    commentCount\n    commentCountV2\n    pcursor\n    rootCommentsV2 {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      hasSubComments\n      likedCount\n      liked\n      status\n      __typename\n    }\n    pcursorV2\n    rootComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      authorLiked\n      subCommentCount\n      subCommentsPcursor\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        likedCount\n        realLikedCount\n        liked\n        status\n        authorLiked\n        replyToUserName\n        replyTo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"},
                          headers=ks_header)
        data = r.json()['data']
        print(data)
        pcursor = data['visionCommentList']['pcursor']
        commentCount=0
        if "commentCountV2" in data['visionCommentList']:
            commentCount=data['visionCommentList']['commentCountV2']
            rrr=requests.post("http://webstt.jiangxisls.com/api/updateTotalCount",
                          json={"videoid":photoId,"totalCount":commentCount})
        rootComments = data['visionCommentList']['rootCommentsV2']
        array = []
        if len(rootComments) > 0:
            for comment in rootComments:
                print(comment)
                # subComments = comment['subComments']
                jj = {}
                jj['platform'] = "快手"
                jj['videoid'] = photoId
                if 'commentId' in comment:
                    jj['comment_id'] = comment['commentId']
                    jj['nickname'] = comment['authorName']
                    jj['content'] = comment['content']
                    jj['comment_time'] = comment['timestamp']
                    array.append(jj)
        print(self.getSendData(array, "快手", False,photoId))
        rt = requests.post("http://webstt.jiangxisls.com/api/postComment",
                               json=self.getSendData(array, "快手", False,photoId))
        if pcursor != "no_more":
            time.sleep(500)
            self.getComment(userid,photoId, pcursor)
        else:
            time.sleep(500)
            self.run()

    def run(self):
        # try:
            res = requests.get("http://webstt.jiangxisls.com/api/getvideo?platform=快手")
            print(res.text)
            aw = res.json()
            if len(aw) > 0:
                rt = requests.post("http://webstt.jiangxisls.com/api/updateVideoStatus",
                           json={"videoid":aw[0]['videoid'],"status":1})
                self.getComment(aw[0]['account'], aw[0]['videoid'], "0")
        # except Exception:
        #     print("错误了")
        #     time.sleep(500)
        #     self.run()


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
