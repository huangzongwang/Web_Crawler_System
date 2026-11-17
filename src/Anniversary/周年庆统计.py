import sys
sys.path.append('../')
import json
import time
from datetime import datetime

import schedule
from xhs import FeedType, XhsClient
import requests

from sentiment import aliyun_oss_comment
from utils import Config, PhoneNumber
from utils import Proxie
from utils.HttpUtil import HttpUtils


class XhsInfoTask():
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
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0  Safari/537.36",
                "Accept": "text/html,application/xhtml+xml, application/xml;q=0 .9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Connection": "keep-alive",
                # "Accept-Encoding": "gzip, deflate, br",
                # "Host": "www.baidu.com",
                # 需要更换Cookie
                "Cookie": "",
            }
            xhs_client = XhsClient(Config.xhs_Cookie7)
            res = requests.get("https://znqcrm.jiangxisls.com/Report/Wapvote2025/get_headquartersvote_list?type=xhs")
            jsoc = res.json()['data']
            for i in jsoc:
                array=[]
                generalize_url_xhs=i['generalize_url_xhs']
                if generalize_url_xhs==None:
                    continue
                print(generalize_url_xhs)
                if i['sales_id']=="0":
                    continue
                # generalize_url_dy=i['generalize_url_dy']
                # print(generalize_url_dy)
                # if len(generalize_url_dy)>5:
                #     generalize_dy_id=""
                #     if generalize_url_dy.__contains__("www.douyin.com/discover"):
                #         generalize_dy_id=generalize_url_dy.replace("https://www.douyin.com/discover?modal_id=","")
                #     else:
                #         req = requests.get(generalize_url_dy, headers=headers, allow_redirects=False)
                #         generalize_dy_id=req.headers.get('Location').split("/?")[0].replace("https://www.iesdouyin.com/share/video/", "")
                #     videoid=generalize_dy_id
                #     print(videoid)
                #     res = HttpUtils().sendGet(url="/api/getkeyvideid?videoid=" + videoid)
                #     if len(res.json()) == 0:
                #         print("-======-----")
                #         res = HttpUtils().sendPost1(json={"videoid": videoid, "status": 1, "url": str(i['id'])}, url="/api/postkey")
                #         print(res.text)
                if len(generalize_url_xhs)>5:
                    print(generalize_url_xhs)
                    generalize_xhs_id=""
                    xsec_token=""
                    if generalize_url_xhs.__contains__("www.xiaohongshu.com/explore"):
                        generalize_xhs_id=generalize_url_xhs.split("?")[0].replace("https://www.xiaohongshu.com/explore/","")
                        if 'xsec_token' in generalize_url_xhs:
                            xsec_token=generalize_url_xhs.split("xsec_token=")[1].split("&")[0]
                        print(xsec_token)
                    elif generalize_url_xhs.__contains__('www.xiaohongshu.com/discovery/item/'):
                        generalize_xhs_id=generalize_url_xhs.split("?")[0].replace("https://www.xiaohongshu.com/discovery/item/","")
                        if 'xsec_token' in generalize_url_xhs:
                            xsec_token=generalize_url_xhs.split("xsec_token=")[1].split("&")[0]
                        print(xsec_token)
                        # req=requests.get(generalize_url_xhs,headers=headers,allow_redirects=False)
                        # if "Location" not in req.headers:
                        #     continue 
                        # if 'xsec_token' in req.headers.get('Location'):
                        #     xsec_token=req.headers.get('Location').split("xsec_token=")[1].split("&")[0]
                        # else:
                        #     continue
                    else:
                        req = requests.get(generalize_url_xhs, headers=headers, allow_redirects=False)
                        print(req.headers)
                        if "Location" in req.headers:
                            if 'xsec_token' in req.headers.get('Location'):
                                xsec_token=req.headers.get('Location').split("xsec_token=")[1].split("&")[0]
                            generalize_xhs_id=req.headers.get('Location').split("?")[0].replace("https://www.xiaohongshu.com/discovery/item/","") 
                    print(generalize_xhs_id)
                    print(xsec_token)
                    print("===========================")
                    
                    if len(xsec_token)==0:
                        array.append({"id":i['id'],"type":"xhs","total_num":0,"xhs_gambit":"","xhs_json":{"upvote":0,"collect":0,"comment":0,"share":0}})
                        url = "https://znqcrm.jiangxisls.com/Report/Wapvote2025/get_headquartersvote_jsonlist"
                        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n"+json.dumps(array)+"\n\r\n-----011000010111000001101001--\r\n\r\n"
                        headers = {"content-type": "multipart/form-data; boundary=---011000010111000001101001"}
                        print(payload)
                        response = requests.request("POST", url, data=payload, headers=headers)
                        print(response.json())
                        continue
                    t = xhs_client.get_note_by_id(generalize_xhs_id,xsec_token=xsec_token)
                    print(t)
                   
                    if "items" in t:
                        items=t['items']
                        if len(items)>0:
                            t=items[0]['note_card']
                    else:
                        if "msg" in t:
                            if t['msg']=="登录已过期":
                                print("=-=====================登录过期了")
                            else:
                                array.append({"id":i['id'],"type":"xhs","total_num":0,"xhs_gambit":"","xhs_json":{"upvote":0,"collect":0,"comment":0,"share":0}})
                    if "interact_info" in t:
                        obj={}
                        interact_info=t['interact_info']
                        liked_count = interact_info['liked_count']
                        collected_count = interact_info['collected_count']
                        comment_count = interact_info['comment_count']
                        share_count = interact_info['share_count']
                        obj['id']=i['id']
                        obj['type']="xhs"
                        obj['total_num']=int(liked_count)+int(collected_count)+int(comment_count)+int(share_count)
                        xhs_json={}
                        xhs_json['upvote']=liked_count
                        xhs_json['collect'] = collected_count
                        xhs_json['comment']=comment_count
                        xhs_json['share']=share_count
                        obj['xhs_gambit']=t['desc']
                        obj['xhs_json']=xhs_json
                        array.append(obj)
                    print(json.dumps(array))
                    url = "https://znqcrm.jiangxisls.com/Report/Wapvote2025/get_headquartersvote_jsonlist"
                    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n"+json.dumps(array)+"\n\r\n-----011000010111000001101001--\r\n\r\n"
                    headers = {"content-type": "multipart/form-data; boundary=---011000010111000001101001"}
                    print(payload)
                    response = requests.request("POST", url, data=payload, headers=headers)
                    print(response.json())
                    time.sleep(10)
        except Exception as e:
            print("-------------")

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.xhsinfo()
        print("这是一个定时任务,更新时间为:" + current_time)

        # 每隔5分钟运行一次job函数

    def run(self):
        schedule.every(1).minutes.do(self.job)
        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()

ks = XhsInfoTask()
ks.run()
