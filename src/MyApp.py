import sys
sys.path.append('../')
from queue import LifoQueue

from src.sentiment.video import celery_baidu_media_task, celery_baidu_news_task, celery_baidu_task, celery_bilbill_task, \
    celery_dy_task, celery_ks_task, celery_sougou_task, celery_toutiao_task, celery_weibo_task, celery_xhs_task
from src.utils.HttpUtil import HttpUtils
from src.utils import Proxie


class MyApplication:
    lifoQueue = LifoQueue()
    index = 0
    proxy = Proxie.Proxie()
    baidutask = celery_baidu_task.BaiduTask()
    bililtask = celery_bilbill_task.BilillTask()
    baijiatask= celery_baidu_news_task.BaijiaTask()
    mediatask= celery_baidu_media_task.MediaTask()
    sougoutask = celery_sougou_task.SouGouTask()
    toutiaotask = celery_toutiao_task.TouTiaoTask()
    dytask = celery_dy_task.DyTask()
    kstask = celery_ks_task.KsTask()
    weibotask = celery_weibo_task.WeiboTask()
    xhstask = celery_xhs_task.xhsTask()
    array = [toutiaotask,bililtask,weibotask, sougoutask]
    keyword = None
    page = 3

    def onSuccess(self, msg, id, count):
        print(self.array[id].getMsg(msg + ",拉取条数为:" + str(count), count))

    def onFinsh(self, id):
        if id < len(self.array):
            self.index = id + 1
            print("-------------------下一个平台")
            if self.index < len(self.array):
                self.lifoQueue.put(
                    self.array[self.index].run(self.keyword, 0, "赛乐赛", self.onSuccess, self.onFail, self.onFinsh,
                                               self.index, self.page), timeout=5)
            else:
                self.index = 0
                self.page = 1
                self.keyword = None
                self.start("赛乐赛")
        else:
            self.index = 0
            self.page = 1
            self.keyword = None
            self.start("赛乐赛")

    def onFail(self, msg, id):
        print(self.array[id].getMsg("拉取失败，错误信息:" + msg, 0))
        msg_data={"title": "weeds测试1","content": {"key值": "采集","key值2": "采集失败","key值3": self.array[id].getMsg("拉取失败，错误信息:" + msg, 0) },"deviceId": "weeds","type": "markdown"}
        respone = HttpUtils().sendPost1(msg_data,"/api/app/navy/task/sendRobotMessage")
        print(respone)
        self.proxy.old_time=0

    def start(self, brand):
        respone = HttpUtils().sendGet("/api/getArticleKeywords?platform=app")
        print(respone.text)
        resultdata = respone.json()
        if len(resultdata) > 0:
            self.keyword = resultdata[0]['keywork']
            self.page = resultdata[0]['pageSize']
        if self.keyword is not None:
            self.lifoQueue.put(
                self.array[self.index].run(self.keyword, 0, brand, self.onSuccess, self.onFail, self.onFinsh,
                                           self.index, self.page), timeout=5)
        else:
            self.start("赛乐赛")
                                           




dycomment = MyApplication()
dycomment.start("赛乐赛")





# if __name__ == '__main__':
#     def food_video():
#         dycomment = MyApplication()
#         dycomment.start("赛乐赛")
#
#
#     scheduler = BlockingScheduler()
#     # # #
#     # # # # 添加任务
#     scheduler.add_job(food_video, 'cron', day_of_week='mon-fri', hour=9, minute=30, end_date='2023-12-31')
#     scheduler.start()
