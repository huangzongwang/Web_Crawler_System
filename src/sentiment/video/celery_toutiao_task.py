import time
from datetime import datetime


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


class TouTiaoTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'

    def getMsg(self, msg, count):
        return "头条爬虫：" + msg + ",条数:" + str(count)

    def toutiao(self, keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count):
        try:
            header = Config.toutiao_header
            param = {
                "keyword": keywork,
                "source": "input",
                "pd": "synthesis",
                "action_type": "pagination",
                "page_num": page,
                # "search_id":"202305171644595FB3718C81D58F825D23",
                "from": "search_tab",
                "cur_tab_title": "search_tab",
                "dvpf": "pc"
            }
            # response1 = proxy.getProxie()
            # print(response1)
            # self.proxles['http'] = 'http://' + response1
            # self.proxles['https'] = 'http://' + response1
            # print(self.proxles)
            url = 'https://so.toutiao.com/search/?' + urlencode(param)
            print(url)
            response = requests.get(url, headers=header)
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find_all('script', type="application/json")
            print(len(data))
            array = []
            if len(data) > 6:
                for i in data:
                    # try:
                    t = json.loads(i.string)
                    print(t)
                    if "data" in t:
                        data = {}
                        data=t['data']
                        if "url" in data:
                            url = data['url']
                            data["url"] = url
                            title = data['title']
                            data['title'] = title
                            if "display" in data:
                                content = data['display']
                                if content!=None and "info" in content:
                                    if "time_factor" in content['info']:
                                        data['time'] = content['info']['time_factor']
                                    else:
                                        data['time'] = ""
                                    if "site_name" in content['info']:
                                        data['user_name'] = content['info']['site_name']
                                    else:
                                        data['user_name'] = ""
                            else:
                                data['time'] = ""
                                data['user_name'] = ""
                            data['content'] = ""
                            data['city'] = "广东"
                            data['mid'] = data['id_str']
                            data['platform'] = "头条"
                            data['keywork'] = keywork
                            data['taskid'] = "0"
                            data['itemid'] = "0"
                            data['brand'] = brand
                            data['status'] = 0
                            data['pageIndex'] = str(page + 1)
                            array.append(data)
                    if "rawData" in t:
                        rawData = t['rawData']
                        if "data" in rawData:
                            data = rawData['data']
                            for item in data:
                                if "merge_article" in item:
                                    merge_article = item['merge_article']
                                    for merge_item in merge_article:
                                        data = {}
                                        url = merge_item['article_url']
                                        data["url"] = url
                                        title = merge_item['title']
                                        data['title'] = title
                                        content = merge_item['abstract']
                                        data['time'] = merge_item['create_time']
                                        data['content'] = content
                                        data['city'] = "广东"
                                        data['mid'] = merge_item['media_creator_id']
                                        data['platform'] = "头条"
                                        data['keywork'] = keywork
                                        data['user_name'] = merge_item['media_name']
                                        data['taskid'] = "0"
                                        data['itemid'] = "0"
                                        data['brand'] = brand
                                        data['status'] = 0
                                        data['pageIndex'] = str(page + 1)
                                        array.append(data)
                                elif "pop_list" in item:
                                    pop_list = item['pop_list']
                                    for pop_item in pop_list:
                                        data = {}
                                        url = pop_item['share_url']
                                        data["url"] = url
                                        title = pop_item['content']
                                        data['title'] = title
                                        data['time'] = pop_item['create_time']
                                        data['content'] = title
                                        data['city'] = "广东"
                                        data['mid'] = pop_item['id']
                                        data['platform'] = "头条"
                                        data['keywork'] = keywork
                                        data['user_name'] = pop_item['media_name']
                                        data['user_url'] = pop_item['user_id']
                                        data['taskid'] = "0"
                                        data['itemid'] = "0"
                                        data['brand'] = brand
                                        data['status'] = 0
                                        data['pageIndex'] = str(page + 1)
                                        array.append(data)
                                else:
                                    data = {}
                                    url = None
                                    if 'url' in item:
                                        url = item['url']
                                    else:
                                        if 'share_url' in item:
                                            url = item['share_url']
                                    title = ""
                                    if "title" in item:
                                        title = item['title']
                                    else:
                                        if 'content' in item:
                                            title = item['content']
                                    id = ""
                                    if 'id' in item:
                                        id = item['id']
                                    media_name = ""
                                    if 'media_name' in item:
                                        media_name = item['media_name']
                                        print(media_name)
                                    create_time = ""
                                    if 'create_time' in item:
                                        create_time = item['create_time']
                                    user_id = ""
                                    if 'user_id' in item:
                                        user_id = item['user_id']

                                    data["url"] = url
                                    title = title
                                    data['title'] = title
                                    data['time'] = create_time
                                    data['content'] = title
                                    data['city'] = "广东"
                                    data['mid'] = id
                                    data['platform'] = "头条"
                                    data['keywork'] = keywork
                                    data['user_name'] = media_name
                                    data['user_url'] = user_id
                                    data['taskid'] = "0"
                                    data['itemid'] = "0"
                                    data['brand'] = brand
                                    data['status'] = 0
                                    data['pageIndex'] = str(page + 1)
                                    if url is not None:
                                        array.append(data)
                analysis = False
                print(array)
                rt = HttpUtils().sendPost2(array, "头条", "/api/postArticle", analysis,keywork=keywork)
                if rt.status_code != 200:
                    msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                                   "key值3": "头条上传数据失败"}, "deviceId": "weeds",
                                "type": "markdown"}
                    respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                    print(respone)
                onsuccess("第" + str(page + 1) + "页拉取成功", index, len(array))
                if page < page_count:
                    time.sleep(500)
                    self.run(keywork=keywork, page=page + 1, brand=brand, onsuccess=onsuccess, onfail=onfail,
                             onfinsh=onfinsh, index=index,
                             page_count=page_count)
                else:
                    time.sleep(500)
                    onfinsh(index)
            else:
                onfail("爬虫失败！！！！被监控了,歇一歇吧", index)
                onfinsh(index)
        except Exception as e:
            onfail(str(e), index)
            onfinsh(index)

    def run(self, keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count):
        self.toutiao(keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count)