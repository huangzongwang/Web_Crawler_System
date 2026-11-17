import sys
sys.path.append('../../')
import time
from datetime import datetime

import requests
import schedule
from baiduspider import BaiduSpider
import re

from utils import Proxie
from utils.HttpUtil import HttpUtils


class BaiduTask():
    proxles = {"http": "http://42.58.35.90:23013", "https": "http://42.58.35.90:23013"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
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
    keyword = None
    page_count = 1
    page_index=0

    def get_real_url(self, v_url):
        """
        获取百度链接真实地址
        :param v_url: 百度链接地址
        :return: 真实地址
        """
        r = requests.get(v_url, headers=self.headers, allow_redirects=False)  # 不允许重定向
        if r.status_code == 302:  # 如果返回302，就从响应头获取真实地址
            real_url = r.headers.get('Location')
        else:  # 否则从返回内容中用正则表达式提取出来真实地址
            real_url = re.findall("URL='(.*?)'", r.text)[0]
        return real_url

    def getMsg(self, msg, count):
        return "百度爬虫：" + msg + ",条数:" + str(count)

    def run_b(self, keywork, page, brand, page_count):
        try:
            print(keywork)
            print(page)
            p=Proxie.Proxie()
            ips=p.gethsProxie()
            if ":" in ips:
                self.proxles["http"]="http://"+ips
                self.proxles["https"]="https://"+ips
            else:
                print(ips)
            
            spider = BaiduSpider()
            print(self.proxles)
            result = spider.search_web(query=keywork,  pn=int(page))
            plain = result.plain
            array = []
            for item in plain:
                if "url" in item:
                    data = {}
                    title = item['title']
                    des = item['des']
                    url = item['url']
                    time1 = item['time']
                    url = self.get_real_url(url)
                    data['status'] = 0

                    # if time1 is not None:
                    #     if "年" in time1:
                    #         s_t = time.strptime(time1, "%Y年%m月%d日")  # 返回元祖
                    #         mkt = int(time.mktime(s_t))
                    #         timeArray = time.localtime(int(mkt))
                    #         time1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    data['platform'] = "百度"
                    data['title'] = title
                    data['url'] = url
                    data['time'] = ""
                    data['city'] = "广东"
                    data['content'] = des
                    data['mid'] = str(int(time.time()))
                    data['keywork'] = keywork
                    data['taskid'] = "0"
                    data['itemid'] = "0"
                    data['brand'] = brand
                    data['pageIndex']=str(page + 1)
                    print(title)
                    array.append(data)
            print(array)
            res=HttpUtils().sendPost2(array, "百度", "/api/postArticle", analysis=False,keywork=keywork)
            print(res.text)
            if res.status_code!=200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "百度上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
            if page < page_count:
                self.page_index = self.page_index + 1
            else:
                self.page_index = self.page_count + 1

        except Exception as e:
            print(e)

    def job(self):
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.keyword == None:
                self.page_index = 0
                respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=%E7%99%BE%E5%BA%A6")
                print(respone.text)
                resultdata = respone.json()
                if len(resultdata) > 0:
                    self.keyword = resultdata[0]['keywork']
            elif self.page_index > self.page_count:
                self.page_index = 0
                self.keyword=None
                respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=%E7%99%BE%E5%BA%A6")
                print(respone.text)
                resultdata = respone.json()
                if len(resultdata) > 0:
                    self.keyword = resultdata[0]['keywork']
            print(self.page_index)
            if self.keyword != None:
                self.run_b(self.keyword, self.page_index, "赛乐赛", self.page_count)
            print("这是一个定时任务,更新时间为:" + current_time)
        except Exception as e:
            print(e)

        # 每隔5分钟运行一次job函数

    def run(self):
            schedule.every(1).minutes.do(self.job)

            while True:
                # 等待1秒钟
                time.sleep(1)
                # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
                schedule.run_pending()


dy=BaiduTask()
# dy.getIp()
dy.run()
