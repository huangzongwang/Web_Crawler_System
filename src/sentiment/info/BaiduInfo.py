import time

from bs4 import BeautifulSoup

from xhs import FeedType, XhsClient
import requests

from src.sentiment import aliyun_oss_comment
from src.utils import Config, PhoneNumber
from src.utils import Proxie
from src.utils.HttpUtil import HttpUtils


class BaiduTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    oss = aliyun_oss_comment.OssService()
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

    def getSendData(self, array, platform):
        dd = {}
        dd["platform"] = platform
        dd["data"] = array
        return dd

    def Baiduinfo(self):
        try:
            res = requests.get("http://webstt.jiangxisls.com/api/getBaiduArtitle")
            jsoc = res.json()[0]
            if len(jsoc) > 0:
                url = jsoc['url']
                if str(url).__contains__("zhuanlan.zhihu"):
                    # 知乎
                    r = requests.get("https://zhuanlan.zhihu.com/p/692737198", headers=self.headers,
                                     allow_redirects=False)
                    soup = BeautifulSoup(r.text, "html.parser")
                    container = soup.find('a', {'class': 'UserLink-link'})
                    print(container['href'])
                    print(container)
                    img = container.find("img", {'class': 'Avatar AuthorInfo-avatar css-1syywx2'})
                    print(img['alt'])
                    url = container['href']
                    name = img['alt']
                    if url is not None:
                        rt = HttpUtils().sendPost1(
                            json={"id": jsoc['id'], "user_url": url, "user_name": name},
                            url="/api/updateUrlAndName")

                elif str(url).__contains__("sohu.com"):
                    # 搜狐
                    r = requests.get("https://www.sohu.com/a/763271257_121877617", headers=self.headers,
                                     allow_redirects=False)
                    soup = BeautifulSoup(r.text, "html.parser")
                    container = soup.find('div', {'class': 'user-info'})
                    a = container.find('h4').find('a')
                    print(a['href'])
                    print(a.text)
                    url = a['href']
                    name = a.text
                    if url is not None:
                        rt = HttpUtils().sendPost1(
                            json={"id": jsoc['id'], "user_url": url, "user_name": name},
                            url="/api/updateUrlAndName")

                elif str(url).__contains__("www.163.com"):
                    # 网易
                    r = requests.get("https://www.163.com/dy/article/I8DQ2KS505563DBK.html", headers=self.headers,
                                     allow_redirects=False)
                    soup = BeautifulSoup(r.text, "html.parser")
                    container = soup.find('div', {'class': 'post_wemedia_avatar'})
                    a = container.find('a')
                    print(a['href'])
                    print(a.find('img')['alt'])
                    url = a['href']
                    name = a.find('img')['alt']
                    if url is not None:
                        rt = HttpUtils().sendPost1(
                            json={"id": jsoc['id'], "user_url": url, "user_name": name},
                            url="/api/updateUrlAndName")

            time.sleep(500)
            self.run()
        except Exception:
            time.sleep(500)
            self.run()
            print("---------------")

    def run(self):

        self.Baiduinfo()


ks = BaiduTask()
ks.run()
