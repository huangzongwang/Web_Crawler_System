import sys
sys.path.append('../../../')
import time

import requests
from src.utils import Config
from src.utils.HttpUtil import HttpUtils


class KsVideo:

    def run(self, url, page, onsuccess, onfail, onfinsh, index):
        print("拉取抖音个人信息,获取抖音视频列表")
        sec_uid = str(url).replace("https://www.kuaishou.com/profile/", '')
        print(sec_uid)
        self.getVideo(sec_uid, page, onsuccess, onfail, onfinsh, index)

    def getMsg(self, msg, count):
        return "快手主页爬虫：" + msg + ",条数:" + str(count)

    def getVideo(self, userid, pcursor):
        try:
            ks_header = Config.ks_login_header
            url = "https://www.kuaishou.com/profile/" + userid
            ks_header['Referer'] = url
            r = requests.post("https://www.kuaishou.com/graphql", json={"operationName": "visionProfilePhotoList",
                                                                        "variables": {"userId": userid,
                                                                                      "pcursor": pcursor,
                                                                                      "page": "profile"},
                                                                        "query": "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n collectCount\n coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n collectCount\n coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"},
                              headers=ks_header)
            print(r.text)
            # data = r.json()['data']
            # pcursor = data['visionProfilePhotoList']['pcursor']
            # rootComments = data['visionProfilePhotoList']['feeds']
            # array = []
            # if len(rootComments) > 0:
            #     for comment in rootComments:
            #         json_note = {}
            #         json_note['platform'] = "快手"
            #         json_note['title'] = comment['photo']['caption']
            #         json_note['url'] = comment['photo']['coverUrl']
            #         json_note['account'] = comment['author']['id']
            #         json_note['videoid'] = comment['photo']['id']
            #         array.append(json_note)
            #         res = HttpUtils().sendGet("/api/get/my/video?aid=" + json_note['videoid'])
            #         print(res.json())
            #         if len(res.json()) > 0:
            #             pcursor = "no_more"
            # if len(array):
            #     rt = HttpUtils().sendPost(array, "快手", "/api/postVideoList", False)
            #     print(rt.text)
            # onsuccess("第" + str(pcursor + 1) + "页拉取成功", index, len(array))
            # if pcursor != "no_more":
            #     time.sleep(300)
            #     self.getVideo(userid, pcursor,onsuccess, onfail, onfinsh, index)
            # else:
            #     time.sleep(500)
            #     onfinsh(index)

        except Exception as e:  
            print("=============错误了")
        
ks=KsVideo()
ks.getVideo('3xnvs7uj2drvgi2',"")