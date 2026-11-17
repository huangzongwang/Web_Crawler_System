import time

import execjs
from apscheduler.schedulers.blocking import BlockingScheduler

import requests

from src.utils import Proxie, aliyun_oss, Config
from urllib.parse import urlencode
import urllib.parse

from src.utils.HttpUtil import HttpUtils


class DyVideo:
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    oss = aliyun_oss.OssService()

    def __init__(self, *args, **kwargs):
        super(DyVideo, self).__init__(*args, **kwargs)

    def getMsg(self, msg, count):
        return "食品爬虫：" + msg + ",条数:" + str(count)

    def dySreach(self, keywork, page, onsuccess, onfail, onfinsh, index):
        try:
            dy_headers = Config.dy_header

            dy_headers['Referer'] = "https://www.douyin.com/search/" + urllib.parse.quote(
                keywork) + "?aid=66bcf4cf-435d-4d8b-9b2f-5a5567fd885c&publish_time=0&sort_type=0&source=normal_search&type=general"

            param = {
                "device_platform": "webapp",
                "aid": 6383,
                "channel": "channel_pc_web",
                "search_channel": "aweme_general",
                "sort_type": 0,
                "publish_time": 0,
                "keyword": keywork,
                "search_source": "normal_search",
                "query_correct_type": 1,
                "from_group_id": "",
                "offset": page,
                "count": 10,
                "pc_client_type": 1,
                "version_code": 190600,
                "version_name": "19.60",
                "cookie_enabled": "false",
                "screen_width": 1920,
                "screen_height": 1080,
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Chrome",
                "browser_version": "113.0.0.0 ",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "",
                "os_name": "Windows",
                "os_version": 10,
                "cpu_core_num": 4,
                "device_memory": 8,
                "platform": "PC",
                "downlink": 10,
                "effective_type": "4g",
                "round_trip_time": 50,
                "webid": "7224418331088242237",

            }
            xbogus = execjs.compile(open('D:\\gy\\py\\Sentiment\\dy_sign_news.js').read()).call('get_xb',
                                                                                                '/aweme/v1/web/general/search/single/?' + urlencode(
                                                                                                    param))
            print(xbogus)
            proxie = Proxie.Proxie()
            response1 = proxie.getProxie()
            self.proxles['http'] = 'http://' + response1
            self.proxles['https'] = 'http://' + response1
            print(self.proxles)
            r = requests.get(
                "https://www.douyin.com" + xbogus,
                headers=dy_headers, proxies=self.proxles)
            json1 = r.json()
            data = json1['data']
            has_more = json1['has_more']
            array = []
            for i in data:
                respon_data = {}
                if "aweme_info" in i:
                    aweme_id = i['aweme_info']['aweme_id']
                    aweme_type = i['aweme_info']['aweme_type']
                    desc = ""
                    if "desc" in i['aweme_info']:
                        desc = i['aweme_info']['desc']
                    create_time = ""
                    if "create_time" in i['aweme_info']:
                        create_time = i['aweme_info']['create_time']
                    nickname = ""
                    if "author" in i['aweme_info']:
                        nickname = i['aweme_info']['author']['nickname']
                    play_addr = ""
                    url = ""
                    if "video" in i['aweme_info']:
                        if "play_addr" in i['aweme_info']['video']:
                            print(play_addr)
                            play_addr = i['aweme_info']['video']['play_addr']['url_list'][0]
                            url = self.oss.postFile(play_addr, aweme_id)
                            print(url)
                    if aweme_type == 68:
                        if "images" in i['aweme_info']:
                            images = i['aweme_info']['images'][0]['download_url_list']
                            url = images[0]
                            print(url)
                    respon_data['videoid'] = aweme_id
                    respon_data['nickname'] = nickname
                    respon_data['imgUrl'] = url
                    respon_data['url'] = play_addr
                    respon_data['title'] = desc
                    respon_data['collectTime'] = create_time
                    respon_data['publishTime'] = create_time
                    array.append(respon_data)
            if len(array) > 0:
                print(array)
                HttpUtils().sendPost(array, "抖音", "/api/postFoodVideos", False)
            onsuccess("第" + str(page + 1) + "页拉取成功", index, len(array))

            if len(data) > 0:
                if page < 30:
                    time.sleep(500)
                    self.dySreach(keywork, page + 10)
                else:
                    onfinsh(index)
            else:
                onfinsh(index)

        except Exception as e:
            onfail(str(e), index)
            onfinsh(index)
