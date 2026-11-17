import subprocess
import time
from datetime import datetime

import execjs

import requests
import schedule

from src.sentiment import aliyun_oss_comment
from src.utils import Proxie, PhoneNumber, Config
from urllib.parse import urlencode
import urllib.parse

from src.utils.HttpUtil import HttpUtils


class DyTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword=None
    page_count=3
    page_index=0
    oss = aliyun_oss_comment.OssService()

    keyword_index=0
    keyword_list = ["赛乐赛 减肥", "赛乐赛 骗子", "赛乐赛 骗局", "赛乐赛 投诉", "赛乐赛", "赛乐赛 没用 ",
                    "赛乐赛 没效果", "赛乐赛 无效", "赛乐赛 坑", "赛乐赛 客服", "赛乐赛不瘦", "赛乐赛 骗", "赛乐赛 退",
                    "赛乐赛 行不行", "赛乐赛 诈骗", "如何投诉 赛乐赛", "用了赛乐赛 没效果", "赛乐赛 骗了多少人",
                    "赛乐赛 受害者", "赛乐赛 骗局曝光", "曝光 赛乐赛", "赛乐赛的真实面目", "赛乐赛 骗钱",
                    "投诉赛乐赛 退钱", "赛乐赛 退款", "赛乐赛在哪里投诉", "赛乐赛 有用吗", "赛乐赛杀猪盘",
                    "为了给老公 赛乐赛", "赛乐赛 为了给老公 "]
    def getMsg(self, msg, count):
        return "抖音爬虫：" + msg + ",条数:" + str(count)

    def get_ab(self,url):
        p = subprocess.Popen(['node', './a_bogus', url], stdout=subprocess.PIPE)
        url = p.stdout.read().strip()
        return url
    def dySreach(self, keywork, page, brand, page_count):
        # try:
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
                "update_version_code"
                "pc_client_type": 1,
                "version_code": 170400,
                "version_name": "17.4.0",
                "cookie_enabled": "false",
                "screen_width": 1920,
                "screen_height": 1080,
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Chrome",
                "browser_version": "125.0.0.0 ",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "125.0.0.0",
                "os_name": "Windows",
                "os_version": 10,
                "cpu_core_num": 20,
                "device_memory": 8,
                "platform": "PC",
                "downlink": 10,
                "effective_type": "4g",
                "round_trip_time": 100,
                "webid": "7365729216689964583",

            }

            res = requests.post("https://ttwid.bytedance.com/ttwid/union/register/",
                        json={"region": "cn", "aid": 1768, "needFid": False, "service": "www.ixigua.com",
                              "migrate_info": {"ticket": "", "source": "node"}, "cbUrlProtocol": "https",
                              "union": True})
            ttwid=res.headers['Set-Cookie'].split(';')[0].replace("ttwid=", "")
            print(ttwid)

            dy_header = {
                "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                "accept": "application/json, text/plain, */*",
                "sec-ch-ua-mobile": "?0",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": f"https://www.douyin.com/?recommend=1",
                "cookie": f"ttwid={ttwid}; douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; home_can_add_dy_2_desktop=%220%22; dy_swidth=1920; dy_sheight=1080;",
                "Priority": "u=1, i"
            }

            # dy_headers['Cookie']=f"ttwid={str(ttwid)}; douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; home_can_add_dy_2_desktop=%220%22; dy_swidth=1920; dy_sheight=1080;",
            # print(dy_headers)

            # url = "https://www.douyin.com" + '/aweme/v1/web/general/search/single/?' + urlencode(param)
            url=f"https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&enable_history=1&keyword={keywork}&search_source=search_history&query_correct_type=1&is_filter_search=0&from_group_id=&offset={offset}&count=10&need_filter_settings=0&search_id=20240528151351D62EC61004DB86084CB1&update_version_code=170400&pc_client_type=1&version_code=190600&version_name=19.6.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=125.0.0.0&browser_online=true&engine_name=Blink&engine_version=125.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7365729216689964583"

            print(self.get_ab(f"{url}"))
            url=self.get_ab(f"{url}")
            # xbogus = execjs.compile(open('D:\\project\\gy\\py\\pythonProject\\src\\assets\\dy_sign_news.js').read()).call('get_xb',
            #                                                                                     '/aweme/v1/web/general/search/single/?' + urlencode(
            #                                                                                         param))
            print(url)
            # self.proxles['http'] = 'http://115.220.47.43:4231'
            # self.proxles['https'] = 'http://115.220.47.43:4231'
            r = requests.get(
                 url,
                headers=dy_headers)
            print(r.text)
            json1 = r.json()
            data = json1['data']
            array = []
            array_user = []
            phone_array = []
            print(len(data))
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
                    image_list_url=""
                    if aweme_type==1:
                        if "images" in i['aweme_info']:
                            images = i['aweme_info']['images'][0]['download_url_list']
                            self.oss.tqdm_download(aweme_id + "_" + str(0) + ".jpg", images[0])
                            url_image = self.oss.pushoss(aweme_id + "_" + str(0) + ".jpg",
                                                         aweme_id + "_" + str(0) + ".jpg")
                            # index_image = index_image + 1
                            image_list_url = image_list_url + url_image + ","
                            # index_image=0
                            # old_url=""
                            # for image99 in images:
                            #     print(image99)
                            #     if image99!=old_url:
                            #         self.oss.tqdm_download(aweme_id +"_"+str(index_image)+ ".jpg", image99)
                            #         url_image = self.oss.pushoss(aweme_id +"_"+str(index_image)+ ".jpg", aweme_id +"_"+str(index_image) + ".jpg")
                            #         print(url_image)
                            #         index_image=index_image+1
                            #         image_list_url=image_list_url+url_image+","
                            #         old_url=image99
                    user_data['status'] = 0
                    user_data['title'] = desc
                    user_data['url'] = "https://www.douyin.com/video/" + aweme_id
                    # timeArray = int(time.localtime(create_time))
                    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    user_data['time'] = create_time
                    user_data['city'] = "广东"
                    user_data['videoType'] = aweme_type
                    user_data['content'] = image_list_url
                    user_data['mid'] = aweme_id
                    user_data['keywork'] = keywork
                    user_data['brand'] = brand
                    user_data['taskid'] = 0
                    user_data['itemid'] = 0
                    user_data['pageIndex'] = str(page + 1)
                    if aweme_type!=101:
                        array_user.append(user_data)
                        array.append(respon_data)

            analysis = False
            print(array_user)
            res=HttpUtils().sendPost(array_user, "抖音", "/api/postArticle", analysis=analysis)
            print(res.text)
            if res.status_code != 200:
                msg_data = {"title": "weeds测试1", "content": {"平台": "抖音", "动作": "采集",
                                                               "结果": "抖音上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
            HttpUtils().sendPost(array, "抖音", "/api/postArticleUser", analysis=analysis)
            if len(phone_array) > 0:
                HttpUtils().sendPost(phone_array, "抖音", "/api/post/phone", analysis=analysis)
            if page < page_count:
                if len(data)>0:
                    self.page_index=self.page_index+1
                else:
                    self.page_index = self.page_index
            else:
                self.page_index = self.page_count + 1

        # except Exception:
        #     print("错误了")
        #     self.getIp()
    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.keyword==None:
            self.page_index = 0
            respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=%E6%8A%96%E9%9F%B3")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata[0]['keywork']
        elif self.page_index>self.page_count:
            self.page_index=0
            self.keyword=None
            respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=%E6%8A%96%E9%9F%B3")
            print(respone.text)
            resultdata = respone.json()
            if len(resultdata) > 0:
                self.keyword = resultdata[0]['keywork']
        if self.keyword!=None:
            self.dySreach(self.keyword, self.page_index, "赛乐赛", self.page_count)
        print("这是一个定时任务,更新时间为:" + current_time)

    # 每隔5分钟运行一次job函数


    def run(self):
        schedule.every(1).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()




dy=DyTask()
# dy.getIp()
dy.run()

