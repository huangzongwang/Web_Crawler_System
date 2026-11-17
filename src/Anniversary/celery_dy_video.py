import re
import time
from urllib.parse import urlencode

import execjs
import requests

from src.utils import Proxie, Config
from src.utils.HttpUtil import HttpUtils


class VideoScraccy:
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}

    def getMsg(self, msg, count):
        return "抖音主页爬虫：" + msg + ",条数:" + str(count)

    def run(self, url, page, onsuccess, onfail, onfinsh, index):
        print("拉取抖音个人信息,获取抖音视频列表")
        sec_uid = str(url).replace("https://www.douyin.com/user/", '')
        print(sec_uid)
        self.getuserId(sec_uid, page, onsuccess, onfail, onfinsh, index)

    def getuserId(self, sec_uid, cursor, onsuccess, onfail, onfinsh, index):
        try:
            proxy = Proxie.Proxie()
            response1 = proxy.getProxie()
            self.proxles['http'] = 'http://' + response1
            self.proxles['https'] = 'http://' + response1
            dy_header = Config.dy_header
            param = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "sec_user_id": sec_uid,
                "max_cursor": cursor,
                "locate_query": "false",
                "show_live_replay_strategy": "1",
                "count": "20",
                "publish_video_strategy_type": "2",
                "pc_client_type": "1",
                "version_code": "170400",
                "version_name": "17.4.0",
                "cookie_enabled": "true",
                "screen_width": "1920",
                "screen_height": "1080",
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Chrome",
                "browser_version": "115.0.0.0",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "115.0.0.0",
                "os_name": "Windows",
                "os_version": "10",
                "cpu_core_num": "4",
                "device_memory": "8",
                "platform": "PC",
                "downlink": "8.8",
                "effective_type": "4g",
                "round_trip_time": "0",
                "webid": "7224418331088242237"
            }
            xbogus = execjs.compile(open('D:\\gy\\py\\Sentiment\\dy_sign_news.js').read()).call('get_xb',
                                                                                                '/aweme/v1/web/aweme/post/?' + urlencode(
                                                                                                    param))
            print(xbogus)
            r = requests.get("https://www.douyin.com" + xbogus, headers=dy_header, proxies=self.proxles)
            data = r.json()
            print(data)

            has_more = data['has_more']
            max_cursor = data['max_cursor']
            aweme_list = data['aweme_list']
            array = []
            for aweme in aweme_list:
                json_note = {}
                json_note['platform'] = "抖音"
                json_note['title'] = aweme['desc']
                json_note['url'] = aweme['share_url']
                json_note['account'] = aweme['author']['uid']
                json_note['videoid'] = aweme['aweme_id']
                array.append(json_note)
                res = HttpUtils().sendGet("/api/get/my/video?aid=" + json_note['videoid'])
                print(res.json())
                if len(res.json()) > 0:
                    has_more = 0
            HttpUtils().sendPost(array, "抖音", "/api/postVideoList", False)
            onsuccess("第" + str(cursor + 1) + "页拉取成功", index, len(array))
            if has_more == 1:
                time.sleep(500)
                self.getuserId(sec_uid, max_cursor, onsuccess, onfail, onfinsh, index)
            else:
                time.sleep(500)
                onfinsh(index)

        except Exception as e:
            print(e)
            onfail(str(e), index)
            onfinsh(index)


