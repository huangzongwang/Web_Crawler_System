# https://www.kuaishou.com/short-video/3xemrmqd4btg63g?utm_source=app_share&utm_medium=app_share&utm_campaign=app_share&location=app_share HTTP/1.1
import requests
from bs4 import BeautifulSoup
import json
import sys
sys.path.append('../')
from utils.HttpUtil import HttpUtils
from src.sentiment import aliyun_oss_comment
import os.path
import shutil
from openpyxl import load_workbook
import requests
import json
import base64
import time

oss = aliyun_oss_comment.OssService()


headers={
    "Host": "www.kuaishou.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": "Google Chrome;v=129, Not=A?Brand;v=8, Chromium;v=129",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "kpf=PC_WEB; clientid=3; did=web_2cf66e376548fe30197b052488feb153; didv=1725266852000; kpn=KUAISHOU_VISION"
}
workbook = load_workbook(filename='C:\\Users\\admin\Desktop\\6855d666.xlsx')
sheet = workbook.active
for row in sheet.iter_rows(values_only=True):
    url=row[1]
    photoid=url.replace('https://www.gifshow.com/fw/photo/','')
    print(photoid)
    response=requests.get('https://www.kuaishou.com/short-video/'+photoid+'?utm_source=app_share&utm_medium=app_share&utm_campaign=app_share&location=app_share',headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all('script')
    data=str(data[1]).replace('<script>window.__APOLLO_STATE__=','').replace(';(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());</script>','')
    js=json.loads(data)
    photoUrl=js['defaultClient']['VisionVideoDetailPhoto:3xemrmqd4btg63g']['photoUrl']
    oss.tqdm_download(photoid+".mp4",
                                  photoUrl)
    if os.path.exists(photoid+".mp4"):
        shutil.copy(photoid+".mp4",'//192.168.0.159/策划部视频共享池/竞品视频/20241017-快手')
    time.sleep(60)


