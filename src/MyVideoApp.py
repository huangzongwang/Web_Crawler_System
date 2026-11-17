import time
import schedule
from datetime import datetime

from src.utils import Proxie
from src.utils.HttpUtil import HttpUtils

proxy = Proxie.Proxie()

def job():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    proxy1=proxy.getProxie()
    print(proxy1)
    respone = HttpUtils().sendGet("/api/getArticleKeywords")
    print(respone.text)
    resultdata = respone.json()
    if len(resultdata) > 0:
        keyword = resultdata[0]['keywork']
        file = open("keywork.txt", 'w')  # 打开文件
        file.write(keyword)  # 写入文本
        file.close()  # 关闭文件
    print("这是一个定时任务,更新时间为:"+current_time)


# 每隔5分钟运行一次job函数
schedule.every(300).minutes.do(job)

while True:
    # 等待1秒钟
    time.sleep(1)
    # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
    schedule.run_pending()