import time
from datetime import datetime

import schedule
from openai import OpenAI

class AiChat:
    #
    client = OpenAI(
        api_key="sk-x0cwou7m3dR3TNwwvrsAC0IxroUweWgyMMRsqAwqrrBBKLcM",
        base_url="https://api.moonshot.cn/v1",
    )
    index = 0

    list = ["地球的自转周期是多少?", "月球呢？", "两个星球自转有什么差别"]
    #
    history = [
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
    ]
    def Chat(self,query, history):
        history += [{
                "role": "user",
                "content": query
        }]
        print(history)
        completion = self.client.chat.completions.create(
                model="moonshot-v1-128k",
                messages=history,
                temperature=0.3,
        )
        result = completion.choices[0].message.content
        history += [{
                "role": "assistant",
                "content": result
        }]
        return result

    def job(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(self.Chat(self.list[self.index], self.history))
        self.index=self.index+1
        print("这是一个定时任务,更新时间为:" + current_time)

            # 每隔5分钟运行一次job函数

    def run(self):
        schedule.every(1).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()
dy=AiChat()
dy.run()