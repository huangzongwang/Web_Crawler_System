import requests

from src.utils import Proxie, Config
from urllib.parse import urlencode
import time

from src.utils.HttpUtil import HttpUtils


class BilillTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    def getMsg(self, msg, count):
        return "B站爬虫：" + msg + ",条数:" + str(count)

    def bilibiliSreach(self, keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count):
        try:
            # response1 = proxy.getProxie()
            # print(response1)
            # self.proxles['http'] = 'http://' + response1
            # self.proxles['https'] = 'http://' + response1
            # print(self.proxles)
            param = {
                "page": page,
                "page_size": "42",
                "keyword": keywork
            }
            print(param)
            url = "https://api.bilibili.com/x/web-interface/search/all/v2?" + urlencode(param)
            print(url)
            r = requests.get(url, headers=Config.bilibili_headers)
            html = r.json()
            results = html['data']['result']
            print(len(results))
            array = []
            array_user = []
            for result in results:
                result_type = result["result_type"]
                if result_type == "video":
                    data = result['data']
                    for j in data:
                        json1 = {}
                        user_data = {}
                        pubdate = j['pubdate']
                        author = j['author']
                        mid = j['mid']
                        arcurl = j['arcurl']
                        title = j['title']
                        aid = j['aid']
                        upic = j['upic']
                        typename = j['typename']

                        json1['id'] = aid
                        json1['mid'] = mid
                        json1['author'] = author
                        json1['upic'] = upic
                        json1['typename'] = typename
                        json1['brand'] = brand
                        json1['taskid'] = "0"
                        json1['itemid'] = "0"

                        text = title
                        user_data['status'] = 0
                        user_data['title'] = title
                        user_data['url'] = arcurl
                        timeArray = time.localtime(pubdate)
                        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        user_data['time'] = otherStyleTime
                        user_data['city'] = "广东"
                        user_data['content'] = ""
                        user_data['mid'] = mid
                        user_data['taskid'] = "0"
                        user_data['itemid'] = "0"
                        user_data['keywork'] = keywork
                        user_data['brand'] = brand
                        user_data['pageIndex'] = str(page + 1)
                        if "赛乐赛" in title:
                            array_user.append(user_data)
                            array.append(json1)

            analysis = False
            res=HttpUtils().sendPost2(array_user, "B站", "/api/postArticle", analysis=analysis,keywork=keywork)
            if res.status_code!=200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "B上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
            HttpUtils().sendPost(array, "B站", "/api/postArticleUser", analysis=analysis)
            onsuccess("第" + str(page + 1) + "页拉取成功", index, len(array_user))
            if page < page_count:
                time.sleep(500)
                self.run(keywork=keywork, page=page + 1, brand=brand, onsuccess=onsuccess, onfail=onfail,
                         onfinsh=onfinsh, index=index,
                         page_count=page_count)
            else:
                time.sleep(500)
                onfinsh(index)
        except Exception as e:
            onfail(str(e), index)
            onfinsh(index)

    def run(self, keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count):
        self.bilibiliSreach(keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count)


