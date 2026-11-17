import time

import requests
from baiduspider import BaiduSpider
import re

from src.utils import Proxie
from src.utils.HttpUtil import HttpUtils


class BaiduTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
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

    def run(self, keywork, page, brand, onsuccess, onfail, onfinsh, index, page_count,proxy):
        try:
            print(keywork)
            print(page)
            response1 = proxy.getProxie()
            print(response1)
            self.proxles['http'] = 'http://' + response1
            self.proxles['https'] = 'http://' + response1
            print(self.proxles)
            spider = BaiduSpider()
            result = spider.search_web(query=keywork,  pn=int(page),proxies=self.proxles)
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

                    if time1 is not None:
                        if "年" in time1:
                            s_t = time.strptime(time1, "%Y年%m月%d日")  # 返回元祖
                            mkt = int(time.mktime(s_t))
                            timeArray = time.localtime(int(mkt))
                            time1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    data['platform'] = "百度"
                    data['title'] = title
                    data['url'] = url
                    data['time'] = time1
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

            res=HttpUtils().sendPost(array, "百度", "/api/postArticle", analysis=False)
            print(res)
            if res.status_code!=200:
                msg_data = {"title": "weeds测试1", "content": {"key值": "采集", "key值2": "采集失败",
                                                               "key值3": "百度上传数据失败"}, "deviceId": "weeds",
                            "type": "markdown"}
                respone = HttpUtils().sendPost1(msg_data, "/api/app/navy/task/sendRobotMessage")
                print(respone)
            onsuccess("第" + str(page + 1) + "页拉取成功", index, len(array))
            if page < page_count:
                time.sleep(300)
                self.run(keywork=keywork, page=page + 1, brand=brand, onsuccess=onsuccess, onfail=onfail,
                         onfinsh=onfinsh, index=index,
                         page_count=page_count,proxy=proxy)
            else:
                time.sleep(300)
                onfinsh(index)


        except Exception as e:
            onfail(str(e), index)
            onfinsh(index)

