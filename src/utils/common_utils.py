# -*- coding: utf-8 -*-
# @Author : lihuiwen
# @Email : huiwennear@163.com
# @Time : 2024/5/23 16:59
import json
import logging
import os
import re
import time
import urllib

import random

import requests
from py_mini_racer import MiniRacer



class CommonUtils(object):
    def __init__(self):


        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

        js_path = "D:\\project\\gy\\py\\pythonProject\\src\\assets\\"
        self.x_bogus_js_path = os.path.join(js_path, 'x_bogus.js')
        self.a_bogus_js_path = os.path.join(js_path, 'a_bogus.js')

        with open(self.x_bogus_js_path, 'r', encoding='utf-8') as f:
            x_bogus_js_code = f.read()
        self.x_bogus_ctx = MiniRacer()
        self.x_bogus_ctx.eval(x_bogus_js_code)

        with open(self.a_bogus_js_path, 'r', encoding='utf-8') as f:
            a_bogus_js_code = f.read()
        self.a_bogus_ctx = MiniRacer()
        self.a_bogus_ctx.eval(a_bogus_js_code)

        self.ac_sign_js_path = os.path.join(js_path, 'ac_sign.js')

    def get_xbogus(self, req_url, user_agent):
        """
        xbogus加密
        :param req_url:
        :param user_agent:
        :return:
        """
        query = urllib.parse.urlparse(req_url).query
        xbogus = self.x_bogus_ctx.call('sign', query, user_agent)
        return xbogus

    def get_abogus(self, req_url, user_agent):
        """
        xbogus加密
        :param req_url:
        :param user_agent:
        :return:
        """
        query = urllib.parse.urlparse(req_url).query
        abogus = self.a_bogus_ctx.call('generate_a_bogus', query, user_agent)
        return abogus


    def get_ms_token(self, randomlength=107):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str


    def get_ttwid_webid(self, req_url):
        # while True:
            try:
                headers = {
                    "User-Agent": self.user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Language": "zh-CN,zh;q=0.9"
                }
                res=requests.post("https://ttwid.bytedance.com/ttwid/union/register/",json={"region":"cn","aid":1768,"needFid":False,"service":"www.ixigua.com","migrate_info":{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":True},headers=headers)
                print(res.headers['Set-Cookie'].split(';')[0].replace("ttwid=",""))
                ttwid_str=res.headers['Set-Cookie'].split(';')[0].replace("ttwid=","")
                res=requests.post("https://mcs.zijieapi.com/webid",json={"app_id":2018,"url":"https://www.douyin.com/","user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","referer":"https://www.douyin.com/","user_unique_id":""},headers=headers)
                print(res.json())
                print(res.json()['web_id'])
                webid=res.json()['web_id']
                
                return ttwid_str, webid
               
            except Exception as e:
                logging.error(e)
                time.sleep(1)