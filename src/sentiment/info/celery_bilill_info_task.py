from functools import reduce
from hashlib import md5
import urllib.parse
import requests
import urllib.parse
import time
from src.utils import PhoneNumber
from src.utils import Proxie, Config
from src.utils.HttpUtil import HttpUtils


class BilillinfoTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    mixinKeyEncTab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]

    def getMixinKey(self, orig: str):
        '对 imgKey 和 subKey 进行字符顺序打乱编码'
        return reduce(lambda s, i: s + orig[i], self.mixinKeyEncTab, '')[:32]

    def encWbi(self, params: dict, img_key: str, sub_key: str):
        '为请求参数进行 wbi 签名'
        mixin_key = self.getMixinKey(img_key + sub_key)
        curr_time = round(time.time())
        params['wts'] = curr_time  # 添加 wts 字段
        params = dict(sorted(params.items()))  # 按照 key 重排参数
        # 过滤 value 中的 "!'()*" 字符
        params = {
            k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
            for k, v
            in params.items()
        }
        query = urllib.parse.urlencode(params)  # 序列化参数
        wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
        params['w_rid'] = wbi_sign
        return params

    def getWbiKeys(self):
        '获取最新的 img_key 和 sub_key'
        resp = HttpUtils().sendGet("/api/getbilillkey")
        data = resp.json()["data"]
        if len(data) > 0:
            return data[0]["img_key"], data[0]["sub_key"]
        resp = requests.get('https://api.bilibili.com/x/web-interface/nav')
        resp.raise_for_status()
        json_content = resp.json()
        img_url: str = json_content['data']['wbi_img']['img_url']
        sub_url: str = json_content['data']['wbi_img']['sub_url']
        img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
        timeArray = time.localtime(time.time())
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        resp = HttpUtils().sendPost({"img_key": img_key, "sub_key": sub_key, "time": otherStyleTime}, "B站",
                                    "/api/postbilbilkey", False)
        return img_key, sub_key


    def bilibiliinfo(self):
        img_key, sub_key = self.getWbiKeys()
        res = HttpUtils.sendGet("/api/getbilbilluser")
        data = res.json()['data']
        if len(data) > 0:
            print(data[0]['mid'])
            print(img_key)
            # https://api.bilibili.com/x/space/wbi/acc/info?mid=538126643&token=&platform=web&web_location=1550101&w_rid=f4431664cfa6607c35d0681db233afc6&wts=1685934376
            signed_params = self.encWbi(
                params={
                    'mid': str(data[0]['mid']),
                    'token': '',
                    'platform': 'web',
                    'web_location': 1550101
                },
                img_key=img_key,
                sub_key=sub_key
            )
            query = urllib.parse.urlencode(signed_params)
            print(query)
            proxy = Proxie.Proxie()
            response1 = proxy.getProxie()
            print(response1)
            self.proxles['http'] = 'http://' + response1
            self.proxles['https'] = 'http://' + response1
            print(self.proxles)
            url = "https://api.bilibili.com/x/space/wbi/acc/info?" + query
            resp = requests.get(url, headers=Config.bilibili_headers, proxies=self.proxles)
            print(resp.text)
            info_data = resp.json()
            data = info_data['data']
            mid = data['mid']
            sign = data['sign']
            if sign == '':
                sign = "未知"
            phone = PhoneNumber.getphone(sign)
            wechat = PhoneNumber.getwechat(sign)
            phone_array = []
            if len(phone) > 0:
                phone = phone[0]
                item3 = {}
                item3['phone'] = phone
                item3['platform'] = "B站"
                item3['mid'] = data[0]['mid']
                item3['taskid'] = data[0]['taskid']
                item3['itemid'] = data[0]['itemid']
                phone_array.append(item3)
                type = 0
                if data[0]['taskid'] != 0:
                    type = 1
            else:
                phone = "查询不到"
            if wechat is None:
                wechat = "查询不到"
            HttpUtils().sendPost({"sign": sign, "mid": mid, "phone": phone, "wechat": wechat}, "B站",
                                 "/api/updatebilbill", False)
            if len(phone_array) > 0:
                HttpUtils().sendPost(phone_array, "B站", "/api/post/phone", False)

    def run(self):
        self.bilibiliinfo()
