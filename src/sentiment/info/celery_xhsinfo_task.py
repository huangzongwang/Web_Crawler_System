import time
import time
import sys
sys.path.append('../../')
from xhs import FeedType, XhsClient
import requests

from sentiment import aliyun_oss_comment
from utils import Config, PhoneNumber
from utils import Proxie
from utils.HttpUtil import HttpUtils


class XhsInfoTask():
    requests_index=0
    requests_select=0
    xhs_cookie=[Config.xhs_Cookie,Config.xhs_Cookie2,Config.xhs_Cookie3,Config.xhs_Cookie4,Config.xhs_Cookie5,Config.xhs_Cookie6,Config.xhs_Cookie7,Config.xhs_Cookie8,Config.xhs_Cookie9]
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    oss = aliyun_oss_comment.OssService()

    def getSendData(self, array, platform):
        dd = {}
        dd["platform"] = platform
        dd["data"] = array
        return dd

    def xhsinfo(self):
        try:
            res = requests.get("http://webstt.jiangxisls.com/api/getXhsData")
            jsoc = res.json()[0]
            # print(jsoc)
            x_cookie=self.xhs_cookie[self.requests_select]
            if self.requests_index>30:
                if self.requests_select<len(self.xhs_cookie):
                    self.requests_select+=1
                else:
                    self.requests_select=0
            x_cookie=self.xhs_cookie[self.requests_select]
            self.requests_index=0
            xhs_client = XhsClient(x_cookie)
            print(x_cookie)
            # print(jsoc['user_id'])
            # r = xhs_client.get_user_info(jsoc['user_id'])

            # userProfile = r['basic_info']
            # user_text = userProfile['desc']
            # red_id = userProfile['red_id']

            # if user_text == '':
            #     user_text = "未知"
            # phone = PhoneNumber.getphone(user_text)
            # wechat = PhoneNumber.getwechat(user_text)
            # phone_array = []
            # if len(phone) > 0:
            #     phone = phone[0]
            #     item3 = {}
            #     item3['phone'] = phone
            #     item3['platform'] = "小红书"
            #     item3['mid'] = jsoc['note_id']
            #     item3['taskid'] = jsoc['taskid']
            #     item3['itemid'] = jsoc['itemid']
            #     phone_array.append(item3)
            # else:
            #     phone = "查询不到"
            # if wechat is None:
            #     wechat = "查询不到"
            # print(phone)
            # print(wechat)
            # re=HttpUtils().sendPost1(json={"sign": user_text, "user_id": jsoc['user_id'], "phone": phone, "wechat": wechat,
            #                "red_id": red_id}, url="/api/xhsuser")
            # print(re.text)
            # if len(phone_array) > 0:
            #     re=HttpUtils().sendPost(phone_array, "小红书", "/api/post/phone", analysis=False)
            #     print(re.text)
            # time.sleep(300)
            print(jsoc['xsec_token'])
            if "xsec_token" not in jsoc:
                self.run()
                print("-------------")
            elif jsoc['xsec_token'] ==None:
                self.run()
                print("------11-------")
            else:
                print("------------1")
                t = xhs_client.get_note_by_id(jsoc['mid'],jsoc['xsec_token'])
                print(t)
                if "msg" in t:
                    if '登录已过期' in t['msg']:
                        print("更换账号")
                        if self.requests_select<len(self.xhs_cookie):
                            self.requests_select+=1
                        else:
                            self.requests_select=0
                t=t["items"][0]["note_card"]
                desc=t['desc']
                image_list=t['image_list']
                image_list_url = ""
                index_image = 0
                print(image_list)
                for image99 in image_list:
                    print(image99)
                    url_image=""
                    if "http" in image99['url']:
                        self.oss.tqdm_download(jsoc['mid'] + "_" + str(index_image) + ".jpg", image99['url'])
                        url_image = self.oss.pushoss(jsoc['mid'] + "_" + str(index_image) + ".jpg",
                                             jsoc['mid'] + "_" + str(index_image) + ".jpg")
                    print(url_image)
                    index_image = index_image + 1
                    image_list_url = image_list_url + url_image + ","
                rt=HttpUtils().sendPost1(json={"videoid": jsoc['mid'],"content": image_list_url,"desc": desc}, url="/api/updateContentAndDesc")
                print(rt.text)
                time.sleep(200)
                self.requests_index+=1
                self.run()
        except Exception as e:
            print(e)
            time.sleep(200)
            self.run()
            print("---------------")

    def run(self):

        self.xhsinfo()


ks = XhsInfoTask()
ks.run()
