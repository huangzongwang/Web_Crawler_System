import time
from datetime import datetime

import schedule

import requests
from baiduspider import BaiduSpider
from pprint import pprint
import re

from src.sentiment import aliyun_oss_comment
from src.utils import Proxie, Config
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json
import urllib.parse
import json
import base64

from src.utils.HttpUtil import HttpUtils


class KsTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword = None
    page_count = 5
    page_index = 0
    searchSessionId=""
    keyword_index = 0
    keyword_list =['大肚腩', '胖子运动', '胖子减肥', '大腿甩一甩']
    oss = aliyun_oss_comment.OssService()
    def getMsg(self, msg, count):
        return "快手爬虫：" + msg + ",条数:" + str(count)

    def ksSreach(self, keywork, page, brand, page_count):
        try:
            ks_header = Config.ks_login_header
            page_index_count=""
            if page==0:
                page_index_count=""
            else:
                page_index_count=str(page)
            print(page_index_count)
            r = requests.post("https://www.kuaishou.com/graphql", json={
                "operationName": "visionSearchPhoto",
                "variables": {
                    "keyword": keywork,
                    "pcursor": page_index_count,
                    "page": "search",
                    "searchSessionId":self.searchSessionId
                },
                "query": "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n"
            }, headers=ks_header)
            data = r.json()
            print(r.text)
            feeds = data['data']['visionSearchPhoto']['feeds']
            searchSessionId=data['data']['visionSearchPhoto']['searchSessionId']
            array = []
            array_user = []
            for feed in feeds:
                # json1 = {}
                # user_data = {}
                # author = feed['author']
                # user_id = author['id']
                # user_name = author['name']
                # user_headerUrl = author['headerUrl']
                photo = feed['photo']
                photo_id = photo['id']
                # photo_caption = photo['caption']
                # photo_originCaption = photo['originCaption']
                if "photoH265Url" in photo:
                    photo_coverUrl = photo['photoH265Url']
                    if len(photo_coverUrl)>10:
                        self.oss.tqdm_download(photo_id + ".mp4", photo_coverUrl)
                    elif "photoUrl" in photo:
                        photo_coverUrl = photo['photoUrl']
                        if len(photo_coverUrl)>10:
                            self.oss.tqdm_download(photo_id + ".mp4", photo_coverUrl)
                elif "photoUrl" in photo:
                    photo_coverUrl = photo['photoUrl']
                    self.oss.tqdm_download(photo_id + ".mp4", photo_coverUrl)

            #     photo_photoUrl = photo['photoUrl']
            #     photo_likeCount = photo['likeCount']
            #     photo_viewCount = photo['viewCount']
            #     photo_realLikeCount = photo['realLikeCount']
            #     photo_timestamp = photo['timestamp']
            #     photo_animatedCoverUrl = photo['animatedCoverUrl']
            #     photo_videoRatio = photo['videoRatio']
            #
            #     json1['user_id'] = user_id
            #     json1['user_name'] = user_name
            #     json1['user_headerUrl'] = user_headerUrl
            #     json1['photo_id'] = photo_id
            #     json1['brand'] = brand
            #     json1['taskid'] = 0
            #     json1['itemid'] = 0
            #
            #     text = photo_caption
            #     user_data['status'] = 0
            #     user_data['title'] = photo_caption
            #     user_data['url'] = "https://www.kuaishou.com/short-video/" + photo_id
            #     timeArray = time.localtime(photo_timestamp / 1000)
            #     otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            #     user_data['time'] = otherStyleTime
            #     user_data['city'] = "广东"
            #     cont = {"photo_originCaption": photo_originCaption, "photo_coverUrl": photo_coverUrl,
            #             "photo_photoUrl": photo_photoUrl, "photo_likeCount": photo_likeCount,
            #             "photo_viewCount": photo_viewCount, "photo_realLikeCount": photo_realLikeCount,
            #             "photo_animatedCoverUrl": photo_animatedCoverUrl, "photo_videoRatio": photo_videoRatio}
            #     user_data['content'] = base64.b64encode(json.dumps(cont, indent=2).encode("utf-8")).decode('utf-8')
            #     user_data['mid'] = photo_id
            #     user_data['keywork'] = keywork
            #     user_data['brand'] = brand
            #     user_data['taskid'] = 0
            #     user_data['itemid'] = 0
            #     user_data['pageIndex'] = str(page + 1)
            #     array_user.append(user_data)
            #     array.append(json1)
            # analysis = False
            # print(array_user)
            # rt = HttpUtils().sendPost(array_user, "快手", "/api/postArticle", analysis=analysis)
            # print(rt.text)
            # if rt.status_code != 200:
            #     msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
            #                                                    "key值3": "快手上传数据失败"}, "deviceId": "weeds",
            #                 "type": "markdown"}
            #     respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
            #     print(respone)
            # rt = HttpUtils().sendPost(array, "快手", "/api/postArticleUser", analysis=analysis)
            # print(rt.text)
            if page < page_count:
                self.page_index = self.page_index + 1
            else:
                self.page_index = self.page_count + 1

        except Exception as e:
            print(e)


    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.keyword == None:
            self.page_index = 0
            self.keyword=self.keyword_list[self.keyword_index]
            self.keyword_index=self.keyword_index+1
            # respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=%E5%BF%AB%E6%89%8B")
            # print(respone.text)
            # resultdata = respone.json()
            # if len(resultdata) > 0:
            #     self.keyword = resultdata[0]['keywork']
        elif self.page_index > self.page_count:
            self.keyword=None
            self.page_index = 0
            self.keyword = self.keyword_list[self.keyword_index]
            self.keyword_index = self.keyword_index + 1
            # respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=%E5%BF%AB%E6%89%8B")
            # print(respone.text)
            # resultdata = respone.json()
            # if len(resultdata) > 0:
            #     self.keyword = resultdata[0]['keywork']
        if self.keyword!=None:
            self.ksSreach(self.keyword, self.page_index, "赛乐赛", self.page_count)
        print("这是一个定时任务,更新时间为:" + current_time)

    # 每隔5分钟运行一次job函数


    def run(self):
        schedule.every(5).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()




dy=KsTask()
dy.run()