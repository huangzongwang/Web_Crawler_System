import sys
sys.path.append('../../')
import os.path
import shutil
import time
from datetime import datetime

import requests
import schedule

from src.sentiment import aliyun_oss_comment
from src.utils.Download import Download
from src.utils.HttpUtil import HttpUtils


class AnniversaryDy:
    oss = aliyun_oss_comment.OssService()
    def postData(self):
        try:

            res = requests.get("https://webstt.jiangxisls.com/api/getkey?status=2")
            re = res.json()
            for i in re:
                if not  os.path.exists(i['videoid'] + ".mp4"):
                    try:
                        self.oss.tqdm_download(i['videoid'] + ".mp4",
                                  i['url'])
                        if os.path.exists(i['videoid'] + ".mp4"):
                            shutil.copy(i['videoid'] + ".mp4",'//192.168.0.159/策划部视频共享池/竞品视频/20250415/')
                            i['status'] = 3
                            res = requests.post("http://webstt.jiangxisls.com/api/postupdatekey", json=i)
                            print(res.text)
                        else:
                            i['status'] = 3
                            res = requests.post("http://webstt.jiangxisls.com/api/postupdatekey", json=i)
                            print(res.text)
                    except Exception as e:
                        print(e)
                        i['status'] = 4
                        res = requests.post("http://webstt.jiangxisls.com/api/postupdatekey", json=i)
                        print(res.text)

        except Exception as err:
            print(err)

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.postData()
        print("这是一个定时任务,更新时间为:" + current_time)

        # 每隔5分钟运行一次job函数

    def run(self):
        schedule.every(5).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()
dy = AnniversaryDy()
dy.run()

# oss = aliyun_oss_comment.OssService()
# oss.tqdm_download("22222.mp4",
#                                  "http://v95-web-sz.douyinvod.com/37ea034a68b7744b6994a7a9aad81114/66bd8bce/video/tos/cn/tos-cn-ve-51/oYty07mXBnz7DcFhtYfDoI1ggLO3EQABjLQhnA/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=4034&bt=4034&cs=0&ds=4&ft=GZnU0RqeffPdXP~ka1jNvAq-antLjrKazVl.Rka~izvzljVhWL6&mime_type=video_mp4&qs=0&rc=NTo7NTY0ZWZlZGQ7ZGQ2NEBpajpxNnE5cmk5cTMzNDYzM0A0YmEzXjIyXzAxXzUyNS9iYSNmbWAyMmRzXmJgLS1kMC9zcw%3D%3D&btag=c0000e00018000&cquery=100B_102v_102u_100o_100w&dy_q=1723687296&feature_id=59cb2766d89ae6284516c6a254e9fb61&l=20240815100136CAD9A137F6BA0354BB57")