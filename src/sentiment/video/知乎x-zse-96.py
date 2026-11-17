"""
__title__ = '23.知乎x-zse-96'
__author__ = '小肩膀教育'
__mtime__ = '2022/1/18'
"""
import execjs,requests

file=open('./x-zse-96.js','r',encoding='utf8').read()
js_code=execjs.compile(file)
sign=js_code.call('sign')
print(sign)
xbogus = execjs.compile(open('D:\\project\\gy\\py\\pythonProject\\src\\assets\\x-zse-96.js').read()).call('get_xzse96',"AFATiXgZ_BWPTtgq6Lp8yI2EWG9iT6W6BgI=|1670475363"
                                                                                                              '/api/v4/search_v3?gk_version=gz-gaokao&t=general&q=%E5%85%8B%E7%BD%97%E5%9C%B0%E4%BA%9A%E5%A5%B3%E7%90%83%E8%BF%B7%E7%88%86%E7%BA%A2&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal')
print(xbogus)
# AdCbYjRRkxiPTles0YSWbuJdDtdx3pTK3rk=|1714983150
# print(xbogus)
url='https://www.zhihu.com/api/v4/search_v3?gk_version=gz-gaokao&t=general&q=%E5%85%8B%E7%BD%97%E5%9C%B0%E4%BA%9A%E5%A5%B3%E7%90%83%E8%BF%B7%E7%88%86%E7%BA%A2&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal'
headers={
    "Host": "www.zhihu.com",
    "Connection": "keep-alive",
    "x-zse-93": "101_3_3.0",
    "sec-ch-ua": "Google Chrome;v=125, Chromium;v=125, Not.A/Brand;v=24",
    "x-requested-with": "fetch",
    "x-zse-96": sign,
    "x-zst-81": "3_2.0VhnTj77m-qofgh3TxTnq2_Qq2LYuDhV80wSL7iUZQ6nxELF0m4fBJCHMiqHPD4S1hCS974e1DrNPAQLYlUefii7q26fp2L2ZKgSfnveCgrNOQwXTt_Fq6DQye8t9DGwT9RFZQAuTLbHP2GomybO1VhRTQ6kp-XxmxgNK-GNTjTkxkhkKh0PhHix_F0kKQuVybuCM-vcLWuoLN9XO4bxOcXO_UUL_WJS18MgGSXSmTbx1PJH9nJXOFH_zuBcK2HS8x9wMBcLMzGOB39Y0Wre_wC3myvNXJwFYKLC1HCo0OgcKk7CYBwCGrgS81u2uPDNMxqVBucV0rLHVagOBng3KTqV824L_kXom7ut1QAOL6QOs",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "Windows",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.zhihu.com/search?type=content&q=%E5%85%8B%E7%BD%97%E5%9C%B0%E4%BA%9A%E5%A5%B3%E7%90%83%E8%BF%B7%E7%88%86%E7%BA%A2",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "_zap=587a5e00-c582-49a0-8a75-41a84af339a4; d_c0=AdCbYjRRkxiPTles0YSWbuJdDtdx3pTK3rk=|1714983150; gdxidpyhxdE=u%5CunCaSWOQYJe1333%5CrMa1AR9a9NW3Bc0mM8gtRdRWAqBzmcxRveTWh7D7B1Eyb%2B4yaI8hh%5C0EzQICgqbsxvQ7%2BdhbztuADs9HTpa7E460y1YA8xEM%5CC9mfeW76GsxA7buelIq%2F1kVBCc%2F5YmRRwJSfeHqC0tGWzC5WSbXXnQV0Dn9vX%3A1717663312932; _xsrf=19a3b50b-04fb-46d6-b24f-cbc86d9124b4; captcha_ticket_v2=2|1:0|10:1718332031|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfZm9JTmpRcVR3d01xdXRCeDh2WmdFMHZzdFBnRjUzOE9sbS5hOHlRU25tRTBob29MUWRSa0dFZVdoajFTMDBhRFJuVWpZSG5vS3htVHJQbTlUZVVDZkk0M0t5TEpMTEhEeFAyTGNhdm5ERkZySjlramRRYnZXRkJ0SEJ3RFkqSEEwNUZMeHlQYkQ0eTFhVDIuRjRmRUI4RTVYRkJwVTZZdnh4cGRSWDhjKjRZcXlXM0w5RC44VEpGR3kzWC5YQk5oblRibEVHR2E4NVJXamN0aFRZSmVTcUxvaFc0aUhKY0ZWVWlmYU9yUWY0WnFBY3dyYkYqZmx2cVZPVHhDNFFwSlJCX2hjZGhjSUR2TDAuQUJFU3VobFhud0xJSElWWDVVUU1YYU1uU1ZGV2tWQ3RvOHMwUzBSalpya3dWOFJHcSpJdnBvU2pNUkhCZnNIa3BRZ0F5bEZoZy4uWmdFYXBndloyLjg4eUFvZkpJRE9ncnpYV015M2o0WVc4MjhuaUNCMi5UR2Q0TWt0LnFmSzM0TFl2NFZQUXlCZXBrblRIbFM5WWR3bkxGV0R2RjBKd2lidG1rd2FsUmd3UWprNHpfVE5OVTZKVWlhZVpKSEdha3FVVm9JQ3lEU1FyNGNzMkNfRWhMb2YxTi5ONkJFaERKZXlsUzBTS2ladG1SWFdqeFBra2N5Y1k3N192X2lfMSJ9|b27421d8845ea3c8694f55891269828caaf693d6471f608900fb94ec4103fcee; captcha_session_v2=2|1:0|10:1718332048|18:captcha_session_v2|88:RkRpdkZUcFJrKzJqdEl3dXR1MG5sVFVSMCtRWmhQNkNlUDF0elBnY1h2Z1B1eE96cGV3Q285dS83aVFLS3RrLw==|f88fd17d6965810eb6eb034feee4fd1d115a65d018145c670a370dc21179d42e; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1716347585,1716890080,1718243490; z_c0=2|1:0|10:1718691856|4:z_c0|92:Mi4xNHp3ckdRQUFBQUFCMEp0aU5GR1RHQ1lBQUFCZ0FsVk5rUGhZWndBTHYzSmdMZG5Yd2phREJoSllWcUxWc0N5bm13|146fd5d70a89fb9e4b9b3e13e6c5598da89f183f0e42ece3d0c0ed8182fcbfcf; BEC=eee8906a1fecdebcee3fda89d6b84517; __zse_ck=001_ZK5m2Ij8yUWmO/jhUV+iNB7cN/1DxjJhe/LJRdyAUucmqbq4NDL2lBWUzLPHimsJTt0ICXYGPK2K+ibV3abx0UMVjmKePFfOCJj9X4HJH2WM2Tw6ttZFLY=Q4uZpqP+2; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1718703899; KLBRSID=d1f07ca9b929274b65d830a00cbd719a|1718703929|1718703866"
}
html=requests.get(url,headers=headers)
print(html.json())