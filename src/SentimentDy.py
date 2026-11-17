
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

oss = aliyun_oss_comment.OssService()
workbook = load_workbook(filename='C:\\Users\\admin\Desktop\\14489449.xlsx')
print(workbook)
sheet = workbook.active
index=0
for row in sheet.iter_rows(values_only=True):
    url=row[0]
    print(url)
    if str(url).startswith('https'):
        res = HttpUtils().sendGet(url="/api/getkeyvideid?videoid=" + str(url).replace('https://www.douyin.com/video/',''))
        print(res.json())
        if len(res.json()) == 0:
            print("-======-----")
            res = HttpUtils().sendPost1(json={"videoid": str(url).replace('https://www.douyin.com/video/',''), "status": 1, "url": str(url)}, url="/api/postkey")
            print(res.text)
    elif str(url).startswith('http'):
        file_path=str(url).replace('http://i.snssdk.com/video/code/1/toutiao/','').replace('?auto_play=1','')
        print(file_path)
        resp=requests.get('http://i.snssdk.com/video/urls/1/toutiao/mp4/'+file_path+'?callback=tt__video__tuluxc')
        print(resp.text)
        data=resp.text.replace('tt__video__tuluxc(','').replace(')','')
        if not data.__contains__('未授权, 禁止访问'):
            data_json=json.loads(data)
            url=base64.b64decode(data_json['data']['video_list']['video_2']['main_url']).decode('utf-8')
            print(url)
            oss.tqdm_download(file_path+".mp4",
                                  url)
            if os.path.exists(file_path+".mp4"):
                shutil.copy(file_path+".mp4",'//192.168.0.159/策划部视频共享池/竞品视频/20240913')
                




