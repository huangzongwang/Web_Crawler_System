import execjs
import requests
import base64
from openpyxl import load_workbook
from openpyxl import Workbook
import json
header={"Host": "insight.oceancus.com",
"Connection": "keep-alive",
"Content-Length": "128",
"x-custom-template-type": "undefined",
"sec-ch-ua-platform": "Windows",
"sec-ch-ua": "Google Chrome;v=143, Chromium;v=143, Not A(Brand;v=24",
"sec-ch-ua-mobile": "?0",
"x-custom-business-line": "SELF_SERVICE",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
"Accept": "application/json",
"x-custom-report-id": "7597650651648246578",
"Content-Type": "application/json",
"Origin": "https://insight.oceancus.com",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty",
"Referer": "https://insight.oceancus.com/apps/dcma/report?bizType=13&businessLine=SELF_SERVICE&is_new_connect=0&is_new_user=0&recordId=6188095&reportId=7597650651648246578&show_more_button=1",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cookie": "passport_csrf_token=25f7302449a19bbba93186957916b01c; passport_csrf_token_default=25f7302449a19bbba93186957916b01c; sid_guard=755cf040d211eb0c9645553815c62e81%7C1768977922%7C5184002%7CSun%2C+22-Mar-2026+06%3A45%3A24+GMT; uid_tt=ec138c020eb243c284c2b2f807a97284; uid_tt_ss=ec138c020eb243c284c2b2f807a97284; sid_tt=755cf040d211eb0c9645553815c62e81; sessionid=755cf040d211eb0c9645553815c62e81; sessionid_ss=755cf040d211eb0c9645553815c62e81; session_tlb_tag=sttt%7C9%7CdVzwQNIR6wyWRVU4FcYugf_________2syxvJpKwEsiE5MADhPOjeWn7-0Dx7jceIzDeqnPQLp4%3D; is_staff_user=false; sid_ucp_v1=1.0.0-KGE1MGQ2ZmZmMGMxODA5MDg4ZGNjMThhMjZmNzJlNWRmOTQyNGU3MDcKFwinq8Cm_PS9AhCC7MHLBhj6CjgBQOsHGgJobCIgNzU1Y2YwNDBkMjExZWIwYzk2NDU1NTM4MTVjNjJlODE; ssid_ucp_v1=1.0.0-KGE1MGQ2ZmZmMGMxODA5MDg4ZGNjMThhMjZmNzJlNWRmOTQyNGU3MDcKFwinq8Cm_PS9AhCC7MHLBhj6CjgBQOsHGgJobCIgNzU1Y2YwNDBkMjExZWIwYzk2NDU1NTM4MTVjNjJlODE"
}
# req=requests.post("https://insight.oceancus.com/apps/operation_platform/backend/external/report/get_report_package_content",headers=header,json={"draft":False,"reportId":"7597650651648246578","bnpmPackageNames":["@byted-dcma/dcma-component-general-atomics-material-list"]})
# print(req.text)

# 方法1: 使用 with 语句（推荐）
# with open("output.txt", "w", encoding="utf-8") as file:
#     file.write(req.text)

# with open("output1.txt", "r", encoding="utf-8") as file:
#     content = file.read()  # 读取所有内容到一个字符串
# js=json.loads(content)
# for js1 in js:


# print(json.dumps(json.loads(content),ensure_ascii=False))
# data=json.loads(content)['data']['@byted-dcma/dcma-component-general-atomics-material-list'][0]['content']
# print(data)
# with open("output1.txt", "w", encoding="utf-8") as file:
#     file.write(data)


# 你好[玫瑰]我是你的专属瘦身顾问徐芳，后期都是由我一对一指导你的瘦身[愉快]

# {"messages": [{"role": "system", "content": "你好，我是赛乐赛客服"}, {"role": "user", "content": "我是農＆機:)防:)"}, {"role": "assistant", "content": "你好[玫瑰]我是你的专属瘦身顾问徐芳，后期都是由我一对一指导你的瘦身[愉快]"}, {"role": "user", "content": "到了再联系你吗"},{"role":"assistant","chosen":"[玫瑰]嗯啦","rejected":"没问题呀，等您拿到赛乐赛，根据情况咱们一起调整方案。要是有任何疑问，随时找我。"}]}
ress=requests.get("https://coze-coding-project.tos.coze.site/coze_storage_7599863520397885491/dialogues_formatted_e732e3ba.json?sign=1770086985-758fcebc51-0-d82e12a30051fbe477c92bfa83ada7e4160c2e60890b7dfaaa14d4bcc7ddd4c1")
print(ress.content)