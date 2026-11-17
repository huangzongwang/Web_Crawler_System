import execjs
import requests
import base64
import aliyun_oss_comment
from openpyxl import load_workbook
from openpyxl import Workbook
workbook = load_workbook(filename="C:\\Users\\admin\\Desktop\\2222.xlsx")
sheet = workbook.active
obj={}
import json
oss = aliyun_oss_comment.OssService()
ks_login_header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "sec-ch-ua":"Google Chrome;v=143, Chromium;v=143, Not A(Brand;v=24",
            "sec-ch-ua-platform":"Windows",
            "sec-fetch-dest":"document",    
            "Cache-Control":"no-cache",
            "Connection": "keep-alive",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
oss.tqdm_download("F:\\invideo\\111.jsonl",
                                  "https://coze-coding-project.tos.coze.site/coze_storage_7599863520397885491/dialogues_lines_fixed_2661ae68.jsonl?sign=1770088979-08b092a6d2-0-236bfa2be3dee18b0af4e06dea6bdc7ccfae42b2faa0888e786a2aac2d2f3e2f")

# index=0
# with open("output.txt", "r", encoding="utf-8") as file:
#     content = file.read()  # 读取所有内容到一个字符串
# print(content)
# data=json.loads(content)['data']['@byted-dcma/dcma-component-general-atomics-material-list'][0]['content']
# print(data)
# with open("output1.txt", "w", encoding="utf-8") as file:
#     file.write(data)
# content=json.loads(data)['group']
# for group in content:
#     xbogus = execjs.compile(open('D:\\project\\gy\\py\\pythonProject\\src\\test.js').read()).call('crc32', group['id'])
#     print(xbogus)
#     red=requests.get(xbogus)
#     d=red.json()
#     if d['data']['status']==10:
#         print(red.text)
#         url=""
#         try:
#             url=base64.b64decode(red.json()['data']['video_list']['video_2']['main_url']).decode('utf-8')
#             print(url)
#         except :
#             url=base64.b64decode(red.json()['data']['video_list']['video_1']['main_url']).decode('utf-8')
#             print(url)
#             print("-------------")
#         oss.tqdm_download("F:\\invideo\\"+group['id']+".mp4",
#                                   url)

# for row in sheet.iter_rows(values_only=True):
#     vid=row[0]
#     print(vid)
#     if vid=="视频id":
#         continue
#     vid=vid.split("vid=")[2]
#     print(vid)
#     xbogus = execjs.compile(open('D:\\project\\gy\\py\\pythonProject\\src\\test.js').read()).call('crc32',
#                                                                                                 vid)
#     print(xbogus)
#     red=requests.get(xbogus)
#     d=red.json()
#     if d['data']['status']==10:
#         print(red.text)
#         url=""
#         try:
#             url=base64.b64decode(red.json()['data']['video_list']['video_2']['main_url']).decode('utf-8')
#             print(url)
#         except :
#             url=base64.b64decode(red.json()['data']['video_list']['video_1']['main_url']).decode('utf-8')
#             print(url)
#             print("-------------")
#         oss.tqdm_download("F:\\invideo\\"+vid+".mp4",
#                                   url)
