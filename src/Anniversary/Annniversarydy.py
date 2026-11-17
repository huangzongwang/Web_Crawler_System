import time
from datetime import datetime

import requests
import schedule
import json

class AnniversaryDy:
    def postData(self):
        res = requests.get("https://webstt.jiangxisls.com/api/getkey?status=4")
        re = res.json()
        array=[]
        for i in re:
            array.append({"id":i['url'],"type":"dy","total_num":0,"dy_gambit":"","dy_json":{"upvote":0,"collect":0,"comment":0,"share":0}})
            # array.append(json.loads(i['url']))
        url = "https://znqcrm.jiangxisls.com/Report/Wapvote2025/get_headquartersvote_jsonlist"
        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n" + json.dumps(array)+ "\n\r\n-----011000010111000001101001--\r\n\r\n"
        headers = {"content-type": "multipart/form-data; boundary=---011000010111000001101001"}
        print(payload)
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.json())
        if response.json()['code'] == '1':
            for i in re:
                i['status'] = 3
                res = requests.post("http://webstt.jiangxisls.com/api/postupdatekey", json=i)
                print(res.text)

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.postData()
        print("这是一个定时任务,更新时间为:" + current_time)

        # 每隔5分钟运行一次job函数

    def run(self):
        schedule.every(1).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()
dy = AnniversaryDy()
dy.run()
