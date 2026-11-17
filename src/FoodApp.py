from apscheduler.schedulers.blocking import BlockingScheduler

from src.sentiment.celery_dy_food_video import DyVideo
from src.utils.HttpUtil import HttpUtils


class MyApplication:
    dyvideo = DyVideo()

    def onSuccess(self, msg, id, count):
        print(self.dyvideo.getMsg(msg + ",拉取条数为:" + str(count), count))

    def onFinsh(self, id):
        self.start()

    def onFail(self, msg, id):
        print(self.dyvideo.getMsg("拉取失败，错误信息:" + msg, 0))

    def start(self):
        re = HttpUtils().sendGet("/api/getFoodKeywords")
        data = re.json()
        print(data)
        if len(data) > 0:
            item = data[0]
            self.dyvideo.dySreach(item['name'], 0, self.onSuccess, self.onFail, self.onFinsh, 0)



myApplication = MyApplication()
myApplication.start()
