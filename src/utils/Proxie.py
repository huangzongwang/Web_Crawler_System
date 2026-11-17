import os
import time

import requests


class Proxie:
    def getProxie(self):
            response1 = requests.get(
                "http://http.tiqu.letecs.com/getip3?neek=f062ae82484923b1&num=1&type=1&pro=&city=0&yys=0&port=1&time=4&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=3&regions=",
            )
            print(response1.text)
            if response1.text.__contains__("您的余额不足"):
                print("余额不足")
                return ""
            elif response1.text.__contains__("请添加白名单"):
                print("白名单没添加")
                detail = response1.json()['msg']
                detail = detail.replace('请添加白名单', '')
                response1 = requests.get(
                    "https://wapi.http.linkudp.com/index/index/save_white?neek=2498044&appkey=1e8adc9c673738d041813e8390534490&white=" + detail.strip(),
                )
                print(response1.text.strip())
                return ""
            return response1.text.strip()

    def gethsProxie(self):
            response1 = requests.get(
                "https://getip.huashengdaili.com/servers.php?session=U56aa4ad20518093420--8d323c954e34d35fa9b5e00b21b0700f&time=3&count=1&type=text&only=1&pw=no&protocol=http&separator=1&iptype=direct&format=null&dev=web",
            )
            print(response1.text)
            if response1.text.__contains__("余额不足"):
                print("余额不足")
                return ""
            elif response1.text.__contains__("暂未添加白名单"):
                print("白名单没添加")
                detail = response1.json()['detail']
                detail = detail.replace('暂未添加白名单，请前往个人中心添加白名单ip(', '')
                detail = detail.replace(')','')
                response1 = requests.get(
                    "https://getip.huashengdaili.com/servers.php?action=get_white_ip&key=U56aa4ad20518093420--8d323c954e34d35fa9b5e00b21b0700f&ip=" + detail.strip(),
                )
                print(response1.text.strip())
                return ""
            return response1.text.strip()


