import time

from xhs import FeedType, XhsClient
import requests
from baiduspider import BaiduSpider
from pprint import pprint
import re

from src.utils import Proxie, Config
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json

from src.utils.HttpUtil import HttpUtils


class SouGouTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'

    def getMsg(self, msg, count):
        return "搜狗爬虫：" + msg + ",条数:" + str(count)

    def sougouSreach(self, keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count):
        try:
            sougou_headers = Config.sougou_headers
            # response1 = proxy.getProxie()
            # print(response1)
            # self.proxles['http'] = 'http://' + response1
            # self.proxles['https'] = 'http://' + response1
            # print(self.proxles)
            param = {
                "query": keywork,
                "page": page,
                "ie": "utf-8"
            }
            url = 'https://www.sogou.com/web?' + urlencode(param)  # + v_keyword + '&pn=' + str(page * 10)
            r = requests.get(url, headers=sougou_headers)
            html = r.text
            print("响应码是:{}".format(r.status_code))
            soup = BeautifulSoup(html, "html.parser")
            result_list = soup.find_all(class_='struct201102')

            array = []
            for v in result_list:
                request_data = {}
                title_data = v.find(class_="vr-title")
                href = title_data.find('a', href=True)['href']
                title = title_data.find('a', href=True).text
                real_title_url = ""
                print(href)
                if href.startswith("http"):
                    r = requests.get(href)
                    real_url = re.findall("URL='(.*?)'", r.text)
                    if len(real_url) > 0:
                        real_title_url = real_url[0]
                else:
                    url = "https://www.sogou.com" + v.find('a', href=True)['href']
                    r = requests.get(url)
                    real_url = re.findall("URL='(.*?)'", r.text)
                    if len(real_url) > 0:
                        real_title_url = real_url[0]
                if len(real_title_url) > 0:
                    request_data['title'] = title
                    request_data['url'] = real_title_url
                starwiki = v.find(class_="star-wiki")
                request_data['content'] = ""
                print(starwiki)
                if starwiki is not None:
                    request_data['content'] = starwiki.text
                fintext = v.find(class_="fz-mid space-txt")
                if fintext is not None:
                    request_data['content'] = fintext.text
                citedata = v.find(class_="cite-date")
                request_data['time'] = ""
                if citedata is not None:
                    print(citedata.text)
                    citedatatime = str(citedata.text)
                    if citedatatime.__len__() > 0:
                        print(citedatatime.__len__())
                        citedatatime = citedatatime.strip()[1:citedatatime.__len__()]
                        s_t = time.strptime(citedatatime.replace(" ", ""), "%Y-%m-%d")  # 返回元祖
                        mkt = int(time.mktime(s_t))
                        timeArray = time.localtime(int(mkt))
                        citedatatime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        print(citedatatime)
                        request_data['time'] = citedatatime
                request_data['mid'] = str(int(time.time()))
                request_data['city'] = "广东"
                request_data['platform'] = "搜狗"
                request_data['keywork'] = keywork
                request_data['brand'] = brand
                request_data['taskid'] = "0"
                request_data['itemid'] = "0"
                request_data['pageIndex'] = str(page + 1)
                request_data['status'] = 0
                if "赛乐赛" in title:
                    array.append(request_data)

            analysis = False
            rt=HttpUtils().sendPost2(array, "搜狗", "/api/postArticle", analysis,keywork=keywork)
            if rt.status_code != 200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "快手上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
            onsuccess("第：" + str(page + 1) + "页拉取成功", index, len(array))
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
        self.sougouSreach(keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count)
