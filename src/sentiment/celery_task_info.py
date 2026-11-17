import requests
import time
from bs4 import BeautifulSoup
import re
from  src.utils import PhoneNumber
import json
from  src.utils import Proxie


class UserInfoTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}

    def getSendData(self, array, platform, analysis):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        return dd

    def runtask(self):
        print("获取任务-------------------")
        url = "http://localhost:5003/api/getSreachresult?limit=1&status=0&platform=getpython&task_type=No"
        req = requests.get(url)
        print(req.text)
        data = req.json()['data']
        if len(data) > 0:
            task = data[0]
            print(task)
            if task['task_type'] == "search_url":
                self.geturluser(task)
            elif task['task_type'] == "search_title":
                print("-")
                # base = celery_base_task.BaseTask()
                # base.baseRun("赛乐赛", 1, task['task_id'], task['content'], task["itemid"])
            elif task['task_type'] == "search_phone":
                self.getphone(task['task_id'], task['content'], task["itemid"])

    def getphone(self, task_id, content, itemid):
        print("-")
        # array = []
        # result = self.getsgk(content,task_id,itemid,int(time.time()))
        # print(result)
        # array.append(result)
        # content = {}
        # content['taskid'] = task_id
        # content['task_result'] = json.dumps(array, indent=2)
        # content['platform'] = "社工库"
        # content['itemid'] = itemid
        # print(content)
        # rt = requests.post("http://localhost:5003/api/postSreachresult", json=self.getSendData(array, "社工库",True))

    def getsgk(self, content, taskid, itemid, mid):
        sg_header = {
            "Host": "privacy.aiuys.com",
            "Connection": "keep-alive",
            "sec-ch-ua": "Not.A/Brand;v=8, Chromium;v=114, Google Chrome;v=114",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://privacy.aiuys.com/?ref=@",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "_ga=GA1.1.977965678.1687167988; _ga_6B8KGX98GZ=GS1.1.1687167987.1.1.1687168596.0.0.0; __gads=ID=cc4089adf25f889a-222803acbfe1004d:T=1687167989:RT=1687168595:S=ALNI_MZ-dRB7ZDGLgcwZVZqAwKdVNfG0rw; __gpi=UID=00000c518741fbf3:T=1687167989:RT=1687168595:S=ALNI_MbesqFi2yxEwSWO9XkvKLR1SI1XLA"
        }
        proxles = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
        res = requests.get("https://privacy.aiuys.com/api/query?value=" + content, proxies=proxles, headers=sg_header)
        data = res.json()['data']
        names = data['names']
        phone_numbers = data['phone_numbers']
        id_numbers = data['id_numbers']
        qq_numbers = data['qq_numbers']
        wb_numbers = data['wb_numbers']
        emails = data['emails']
        addresses = data['addresses']
        result = {}
        result['taskid'] = taskid
        result['itemid'] = itemid
        result['platform'] = "社工库"
        result['mid'] = mid
        if len(names) > 0:
            result['name'] = names[0]
        if len(phone_numbers) > 0:
            result['phone_number'] = phone_numbers[0]
        if len(id_numbers) > 0:
            result['id_number'] = id_numbers[0]
        if len(qq_numbers) > 0:
            result['qq_number'] = qq_numbers[0]
        if len(wb_numbers) > 0:
            result['wb_number'] = wb_numbers[0]
        if len(emails) > 0:
            result['email'] = emails[0]
        if len(addresses) > 0:
            result['addresse'] = addresses[0]
        return result
        # "https://m.weibo.cn/u/6030603111"

    def geturluser(self, task):
        if task['task_platform'] == "快手":
            self.ksinfo(task['content'], task['task_id'], task["itemid"])
        elif task['task_platform'] == "抖音":
            self.getdyurl(task['content'], task['task_id'], task["itemid"])

    def getdyurl(self, url, taskid, itemid):

        dy_headers = {
            "Host": "www.douyin.com",
            "Connection": "keep-alive",
            "sec-ch-ua": "Google Chrome;v=113, Chromium;v=113, Not-A.Brand;v=24",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            # "Referer": "https://www.douyin.com/search/%E8%B5%9B%E4%B9%90%E8%B5%9B%E9%AA%97%E5%B1%80?aid=66bcf4cf-435d-4d8b-9b2f-5a5567fd885c&publish_time=0&sort_type=0&source=normal_search&type=general",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie": "douyin.com; device_web_cpu_core=4; device_web_memory_size=8; webcast_local_quality=null; ttwid=1%7CFeLXm4hkPtkR13KZY5Wr_dulSxmTACzIkfoTbRs1OrA%7C1682065980%7Cdf0b03f00bc115fb03c814b495dc93c93f4135748e4551300e6266d276ff9602; d_ticket=6812d18432bfda0d79a1185282dc7b36bb89e; xgplayer_user_id=147380391532; douyin.com; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNzciI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbk1JSUJEakNCdFFJQkFEQW5NUXN3Q1FZRFZRUUdFd0pEVGpFWU1CWUdBMVVFQXd3UFltUmZkR2xqYTJWMFgyZDFcclxuWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRS9jRGp1dGNKQ3dIRmFjVjJJWVoraUZXQlxyXG5DUDVXV2pvTHYyZnd2SVpvRXE1QlNseXl6VytEa2RXZnQzMm42OG5XUFgzTVMyOFZtdDg2MTNua3JwUUN3cUFzXHJcbk1Db0dDU3FHU0liM0RRRUpEakVkTUJzd0dRWURWUjBSQkJJd0VJSU9kM2QzTG1SdmRYbHBiaTVqYjIwd0NnWUlcclxuS29aSXpqMEVBd0lEU0FBd1JRSWdOUXJmRDB3LytyWGhGeGdJdDBnMHROQzN2RG9SOStkT2djVlFRYXc4bGRRQ1xyXG5JUUNvVFl5UGoxQ2JUbzlqWjFJWGtnVTdMN3VXekFtSmpqTHhBNDhrd1hzcTNBPT1cclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; passport_csrf_token=4519a41163c4f6495493fb6ac72353af; passport_csrf_token_default=4519a41163c4f6495493fb6ac72353af; s_v_web_id=verify_ljcbl8c4_gegXAbP2_G0wO_4J9W_BBhT_b0puyfhoF9WA; pwa2=%223%7C1%7C3%7C0%22; __ac_nonce=064a7c6d400f3383fb255; __ac_signature=_02B4Z6wo00f010jKKeAAAIDCK8DpijTqf09I6i1AALagJbuOWTj3TGKaLObiwXSSnbCrpgEDqmCk4R7aVOZrLeNfVgwBQXI1ArWOoZR77jJ8Klhwbu28ohytOtlpXMxUr5CMCSBnKtmEF48X7f; strategyABtestKey=%221688717018.417%22; __bd_ticket_guard_local_probe=1688717018790; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; download_guide=%223%2F20230707%2F1%22; msToken=xrHZfsGbAHhyFR7wYdbocNtvDrY7edN4dNnOV6fX6xLPwagQp1PO5vv_XK7_lHHRz5h7l_DtT4BdF60BUI1lf_BBL-qlat3i-L1Iio7KTGfKgfaFqnpW8zvdUX8bYQs=; msToken=2tOYkJNOY9XKq4-gRdyC9dz5kXHnxN0UKMrNBWv5yzhCtFWrs24Us8xhkF-I7AAqY4_M2zfMXh_54iOT8zpWySymNzK9zwfXvDSjHVwC8o5UEAXEKTxsNNz-ddLYdQc=; home_can_add_dy_2_desktop=%221%22; tt_scid=6FenyiGQw1g8metjac9BbrBIgfW4lbEtLoGEbH-bWO-aQuaM9KFegcOCCmGOOpVtdce8"
        }
        proxy = Proxie.Proxie()
        response1 = proxy.getProxie()
        print(response1)
        self.proxles['http'] = 'http://' + response1
        self.proxles['https'] = 'http://' + response1
        print(self.proxles)
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36 Edg/103.0.1264.62'
        }
        print(url)
        ree = requests.get(url, headers=headers)
        print(ree.text)
        # 对页面进行重定向处理 获取新的短视频链接
        new_url = ree.url
        # https://www.iesdouyin.com/share/video/7119013227169598754/?region=CN&mid=7119013266652285726&u_code=jdeie942&did=MS4wLjABAAAAaEl_MkpKRQQPoq06DAgPkUuQk8GsfUm8kn-He5q0h9FXhXqqi1RA5CE6_r0ngjn6&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ&with_sec_did=1&titleType=title&from=web_code_link
        # 7119013227169598754 即为视频 id
        # print(new_url)
        # 使用正则提取id
        id = re.search(r'/video/(.*?)/', new_url).group(1)
        url = 'https://www.douyin.com/video/' + id
        print(url)
        ree = requests.get(url, headers=dy_headers, proxies=self.proxles)
        soup = BeautifulSoup(ree.text, "html.parser")
        data = soup.find_all(class_="owClatq2")
        userurl = data[0].find('a', href=True)['href']
        print(userurl)
        data = soup.find_all(class_="Nu66P_ba")
        title = data[0].text
        ree = requests.get("https:" + userurl, headers=dy_headers, proxies=self.proxles)
        print(ree.text)
        soup = BeautifulSoup(ree.text, "html.parser")
        data = soup.find_all(class_="TxoC9G6_")
        fans = data[1].text
        data = soup.find_all(class_="aH7rLkZZ")
        userid = data[0].text
        data = soup.find_all(class_="a83NyFJ4")
        city = data[0].text
        data = soup.find_all(class_="Nu66P_ba")
        nickname = data[0].text
        desc=""
        if len(data)>1:
            desc = data[1].text
            print(desc)
        data = soup.find_all(class_="J6IbfgzH")
        works = data[0].text
        phone = PhoneNumber.getphone(desc)
        print(phone)
        wechat = PhoneNumber.getwechat(desc)
        phone_array = []
        if len(phone) > 0:
            phone = phone[0]
            item5 = {}
            item5['phone'] = phone
            item5['platform'] = "抖音"
            item5['mid'] = id
            item5['taskid'] = taskid
            item5['itemid'] = itemid
            phone_array.append(item5)
        else:
            phone = "查询不到"
        if wechat is None:
            wechat = "查询不到"
        data = {}
        data['taskid'] = taskid
        data['itemid'] = itemid
        data['platform'] = "抖音"
        data['userid'] = userid.replace('抖音号：', '')
        data['nickname'] = nickname
        data['title'] = title
        data['fans'] = fans
        data['mid'] = id
        data['city'] = city
        data['works'] = works
        data['phone'] = phone
        data['wechat'] = wechat
        data['gender'] = ""

        array = []
        array.append(data)
        # content = {}
        # content['taskid'] = taskid
        # content['task_result'] = json.dumps(array, indent=2)
        # content['platform'] = "抖音"
        # content['itemid'] = itemid
        # print(content)
        rt = requests.post("http://localhost:5003/api/postSreachresult", json=self.getSendData(array, "抖音", True))
        print(rt.text)
        if len(phone_array) > 0:
            requests.post('http://localhost:5003/api/post/phone',
                          json=self.getSendData(phone_array,
                                                "抖音", False))
        # base = celery_base_task.BaseTask()
        # base.baseRun("赛乐赛", 1, taskid, title, itemid)

    def ksinfo(self, url, taskid, itemid):
        ks_header = {
            "Host": "www.kuaishou.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": "Google Chrome;v=113, Chromium;v=113, Not-A.Brand;v=24",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie": "kpf=PC_WEB; clientid=3; did=web_e6e13ee6a2fd2fea429df434254e12a7; didv=1686711708000; kpn=KUAISHOU_VISION"
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36 Edg/103.0.1264.62'
        }
        ree = requests.get(url, headers=headers)
        new_url = ree.url
        print(new_url)
        photostartindex = new_url.rfind("photo/", 0, len(new_url))
        photoendindex = new_url.rfind("?", 0, len(new_url))
        id = new_url[photostartindex + len("photo/"):photoendindex]
        print(id)
        startindex = new_url.rfind("userId=", 0, len(new_url))
        userid = new_url[startindex + len("userId="):startindex + len("userId=") + 15]
        print(userid)
        ree = requests.get("https://www.kuaishou.com/short-video/" + id + "?userId=" + userid, headers=ks_header)
        print(ree.text)
        soup = BeautifulSoup(ree.text, "html.parser")
        data = soup.find_all(class_="video-info-title")
        title = data[0].text
        print(title)

        ks_header = {
            "Host": "www.kuaishou.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": "Google Chrome;v=113, Chromium;v=113, Not-A.Brand;v=24",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie": "kpf=PC_WEB; clientid=3; did=web_e6e13ee6a2fd2fea429df434254e12a7; didv=1686711708000; kpn=KUAISHOU_VISION"
        }

        res = requests.get("http://localhost:5003/api/getksuser")
        jsoc = res.json()['data'][0]
        url = "https://www.kuaishou.com/profile/" + jsoc['user_id']
        ks_header['Referer'] = url
        r = requests.post("https://www.kuaishou.com/graphql", json={
            "operationName": "visionProfile", "variables": {"userId": jsoc['user_id']},
            "query": "query visionProfile($userId: String) {\n  visionProfile(userId: $userId) {\n    result\n    hostName\n    userProfile {\n      ownerCount {\n        fan\n        photo\n        follow\n        photo_public\n        __typename\n      }\n      profile {\n        gender\n        user_name\n        user_id\n        headurl\n        user_text\n        user_profile_bg_url\n        __typename\n      }\n      isFollowing\n      __typename\n    }\n    __typename\n  }\n}\n"
        }, headers=ks_header)
        data = r.json()
        userProfile = data['data']['visionProfile']['userProfile']['profile']
        gender = userProfile['gender']
        user_name = userProfile['user_name']
        user_id = userProfile['user_id']
        headurl = userProfile['headurl']
        user_text = userProfile['user_text']
        phone = PhoneNumber.getphone(user_text)
        wechat = PhoneNumber.getwechat(user_text)
        phone_array = []
        if len(phone) > 0:
            phone = phone[0]
            item5 = {}
            item5['phone'] = phone
            item5['platform'] = "快手"
            item5['mid'] = id
            item5['taskid'] = taskid
            item5['itemid'] = itemid
            phone_array.append(item5)

        else:
            phone = "查询不到"
        if wechat is None:
            wechat = "查询不到"

        data = {}
        data['taskid'] = taskid
        data['itemid'] = itemid
        data['platform'] = "快手"
        data['userid'] = user_id
        data['nickname'] = user_name
        data['title'] = title
        data['fans'] = "0"
        data['city'] = ""
        data['works'] = ""
        data['phone'] = phone
        data['mid'] = id
        data['wechat'] = wechat
        data['gender'] = gender

        # data = {}
        # data['title'] = title
        # data['gender'] = gender
        # data['user_name'] = user_name
        # data['user_id'] = user_id
        # data['headurl'] = headurl
        # data['user_text'] = user_text
        # data['phone'] = phone
        # data['wechat'] = wechat
        array = []
        array.append(data)
        # content = {}
        # content['taskid'] = taskid
        # content['task_result'] = json.dumps(array, indent=2)
        # content['platform'] = "快手"
        # content['itemid'] = itemid
        rt = requests.post("http://localhost:5003/api/postSreachresult", json=self.getSendData(array, "快手", True))
        print(rt.text)
        if len(phone_array) > 0:
            requests.post('http://localhost:5003/api/post/phone',
                          json=self.getSendData(phone_array,
                                                "快手", False))
        # base = celery_base_task.BaseTask()
        # base.baseRun("赛乐赛", 1, taskid, title, itemid)


if __name__ == '__main__':
    userinfo = UserInfoTask()
    userinfo.runtask()
