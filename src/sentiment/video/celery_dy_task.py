import sys
sys.path.append('../../')
import time

import execjs

import requests

from utils import Proxie, PhoneNumber, Config
from urllib.parse import urlencode
import urllib.parse

from utils.HttpUtil import HttpUtils


class DyTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    def getMsg(self, msg, count):
        return "抖音爬虫：" + msg + ",条数:" + str(count)

    def dySreach(self, keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count,proxy):
        try:
            dy_headers = Config.dy_header
            dy_headers['Referer'] = "https://www.douyin.com/search/" + urllib.parse.quote(
                keywork) + "?publish_time=0&sort_type=2&type=general"
            if page==0:
                offset=0
            else:
                offset=page*10
            param = {
                "device_platform": "webapp",
                "aid": 6383,
                "channel": "channel_pc_web",
                "search_channel": "aweme_general",
                # "search_channel": "aweme_video_web",
                "sort_type": 2,
                "publish_time": 0,
                "keyword": keywork,
                "search_source": "normal_search",
                "query_correct_type": 1,
                "from_group_id": "",
                "offset":offset,
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
                "round_trip_time": 100,
                "webid": "7224418331088242237",

            }
            xbogus = execjs.compile(open('D:\\gy\\py\\Sentiment\\dy_sign_news.js').read()).call('get_xb',
                                                                                                '/aweme/v1/web/general/search/single/?' + urlencode(
                                                                                                    param))
            print(xbogus)
            response1 = proxy.getProxie()
            self.proxles['http'] = 'http://' + response1
            self.proxles['https'] = 'http://' + response1
            r = requests.get(
                "https://www.douyin.com" + xbogus,
                headers=dy_headers,proxies=self.proxles)
            json1 = r.json()
            data = json1['data']
            array = []
            array_user = []
            phone_array = []
            for i in data:
                respon_data = {}
                user_data = {}
                if "aweme_info" in i:
                    aweme_type = 0
                    if "aweme_type" in i['aweme_info']:
                        aweme_type = i['aweme_info']['aweme_type']
                        if aweme_type == 68:
                            aweme_type = 1
                    aweme_id = ""
                    if "aweme_id" in i['aweme_info']:
                        aweme_id = i['aweme_info']['aweme_id']
                    desc = ""
                    if "desc" in i['aweme_info']:
                        desc = i['aweme_info']['desc']
                    create_time = ""
                    if "create_time" in i['aweme_info']:
                        create_time = i['aweme_info']['create_time']
                    uid = ""
                    short_id = ""
                    nickname = ""
                    signature = ""
                    unique_id = ""
                    enterprise_verify_reason = ""
                    sec_uid = ""
                    avatar_larger = ""
                    following_count = ""
                    follower_count = ""
                    if "author" in i['aweme_info']:
                        author = i['aweme_info']['author']
                        if "uid" in author:
                            uid = author['uid']
                        if "short_id" in author:
                            short_id = author['short_id']
                        if "nickname" in author:
                            nickname = author['nickname']
                        if "signature" in author:
                            signature = author['signature']
                        if "unique_id" in author:
                            unique_id = author['unique_id']
                        if "enterprise_verify_reason" in author:
                            enterprise_verify_reason = author['enterprise_verify_reason']
                        if "sec_uid" in author:
                            sec_uid = author['sec_uid']
                        if "avatar_larger" in author:
                            avatar_larger = author['avatar_larger']['uri']
                        if "following_count" in author:
                            following_count = author['following_count']
                        if "follower_count" in author:
                            follower_count = author['follower_count']
                    signature = signature.rstrip()
                    if signature == '':
                        signature = "未知"
                    phone = PhoneNumber.getphone(signature)
                    wechat = PhoneNumber.getwechat(signature)
                    if len(phone) > 0:
                        phone = phone[0]
                        item5 = {}
                        item5['phone'] = phone
                        item5['platform'] = "抖音"
                        item5['mid'] = aweme_id
                        item5['taskid'] = 0
                        item5['itemid'] = 0
                        phone_array.append(item5)
                    else:
                        phone = "查询不到"
                    if wechat is None:
                        wechat = "查询不到"
                    respon_data["aweme_id"] = aweme_id
                    respon_data["uid"] = uid
                    respon_data["short_id"] = short_id
                    respon_data["nickname"] = nickname
                    respon_data["signature"] = signature
                    respon_data["unique_id"] = unique_id
                    respon_data['phone'] = phone
                    respon_data['wechat'] = wechat
                    respon_data["enterprise_verify_reason"] = enterprise_verify_reason
                    respon_data["sec_uid"] = sec_uid
                    respon_data['brand'] = brand
                    respon_data['pic'] = "https://p3-pc.douyinpic.com/aweme/" + avatar_larger
                    respon_data['following_count'] = following_count
                    respon_data['follower_count'] = follower_count
                    respon_data['taskid'] = 0
                    respon_data['itemid'] = 0

                    user_data['status'] = 0
                    user_data['title'] = desc
                    user_data['url'] = "https://www.douyin.com/video/" + aweme_id
                    timeArray = time.localtime(create_time)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    user_data['time'] = otherStyleTime
                    user_data['city'] = "广东"
                    user_data['videoType'] = aweme_type
                    user_data['content'] = ""
                    user_data['mid'] = aweme_id
                    user_data['keywork'] = keywork
                    user_data['brand'] = brand
                    user_data['taskid'] = 0
                    user_data['itemid'] = 0
                    user_data['pageIndex'] = str(page + 1)
                    array_user.append(user_data)
                    array.append(respon_data)

            analysis = False
            print(array_user)
            res=HttpUtils().sendPost(array_user, "抖音", "/api/postArticle", analysis=analysis)
            if res.status_code != 200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "抖音上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
            HttpUtils().sendPost(array, "抖音", "/api/postArticleUser", analysis=analysis)
            if len(phone_array) > 0:
                HttpUtils().sendPost(phone_array, "抖音", "/api/post/phone", analysis=analysis)
            onsuccess("第" + str(page + 1) + "页拉取成功", index, len(array_user))
            if page < page_count:
                time.sleep(500)
                self.run(keywork=keywork, page=page + 1, brand=brand, onsuccess=onsuccess, onfail=onfail,
                         onfinsh=onfinsh, index=index,
                         page_count=page_count,proxy=proxy)
            else:
                time.sleep(500)
                onfinsh(index)
        except Exception as e:
            onfail(str(e), index)
            onfinsh(index)

    def run(self, keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count,proxy):
        self.dySreach(keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count,proxy)
