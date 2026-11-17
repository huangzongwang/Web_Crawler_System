import os.path
import shutil
import time
from datetime import datetime
import sys
sys.path.append('../')
import requests
import schedule

from sentiment import aliyun_oss_comment
from utils.Download import Download
from utils.HttpUtil import HttpUtils
import json


class AnniversaryDy:
    oss = aliyun_oss_comment.OssService()
    def postData(self):
        try:

            # res = requests.get("https://webstt.jiangxisls.com/api/getkey?status=2")
            # re = res.json()
            # url = re[0]['url']
            # videoid=re[0]['videoid']
            # url_json = json.loads(url)
            # url1 = url_json['url']
            # print(url1)
            # dy_header = {
            #     "Host": "www.douyin.com",
            #     "Connection": "keep-alive",
            #     "sec-ch-ua": "Google Chrome;v=125, Chromium;v=125, Not.A/Brand;v=24",
            #     "Accept": "application/json, text/plain, */*",
            #     "sec-ch-ua-mobile": "?0",
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            #     "sec-ch-ua-platform": "Windows",
            #     "Sec-Fetch-Site": "same-origin",
            #     "Sec-Fetch-Mode": "cors",
            #     "Sec-Fetch-Dest": "empty",
            #     "Referer": "https://www.douyin.com/video/7364765039644921114",
            #     "Accept-Language": "zh-CN,zh;q=0.9",
            #     "Cookie": "ttwid=1%7CsR3rVSba0OrXdyijyymHeC_1u6vSLwUv5N8NGPpig9k%7C1714967493%7Cfaf2e90ab915026717b74cb09dd113d64d400941e19ae77f2a2ef687e21002a6; bd_ticket_guard_client_web_domain=2; SEARCH_RESULT_LIST_TYPE=%22single%22; UIFID_TEMP=29d6bea3e5a6c157a08a212e1912b5e8a78666ece26be56100fa19e58a63a45b18e84b3c21d3f0f2b0f9ecc0aa58a67b1a248997f136535c26be30cf2ecff98ae546654ac99fe76365c79f7cb3994507; UIFID=29d6bea3e5a6c157a08a212e1912b5e8a78666ece26be56100fa19e58a63a45b6eec83a382132c2e52db5f2690dac763acd13c00f881883c0ee0d84769895280113c48b2ee54218bc6d2b6f820feadbf9e5ade60a74f69134df9ceda19bc10d0aa769c11c7c2ea29ebfbe11fb48b8053d2e8129ce35a13edeb972fea2a54bf4c40117ac3b23185f815705c6d4ed5770d4e9daa72f124e1ead5e71b1987219689; passport_csrf_token=564233cf2141c710636e7baec83c6b44; passport_csrf_token_default=564233cf2141c710636e7baec83c6b44; is_staff_user=false; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; store-region-src=uid; my_rd=2; d_ticket=a053c4387185e76d4ddac3d17427b71c9f7e4; passport_assist_user=CjyrK0Iw7xS37U3wJJHXRji_fJe_hQmlTkSTKNcnwWYzy8rVIMlYZjkLY4GThzB6_sayJkDmiAraTM6NFpQaSgo8A1IA9PQZ5SvATiXe4hMUKP2Bnaah34QETTcqcAj-on-cL4mR0vcSU0PAoj2B-SvPIboz0iEWchgNfx_VELvW1w0Yia_WVCABIgEDaD4vIw%3D%3D; n_mh=eqGn3kR2aKQuug3nOv98c5xP01S4w0EjSO78rjf1mNA; sso_uid_tt=7e4a40eebfaf590a66bc22c9339cfb1b; sso_uid_tt_ss=7e4a40eebfaf590a66bc22c9339cfb1b; toutiao_sso_user=df1e7d7cc86a53b4ff5fcb82e2ad76e4; toutiao_sso_user_ss=df1e7d7cc86a53b4ff5fcb82e2ad76e4; sid_ucp_sso_v1=1.0.0-KDQ2OTQxMDhlMzVjMGFjMWI2OTdlYWIyNWYzMWRhYzk4NDlkOTA2OWEKHwiE5aKzjgIQ2ruNtQYY7zEgDDCP5ZvPBTgCQPEHSAYaAmxmIiBkZjFlN2Q3Y2M4NmE1M2I0ZmY1ZmNiODJlMmFkNzZlNA; ssid_ucp_sso_v1=1.0.0-KDQ2OTQxMDhlMzVjMGFjMWI2OTdlYWIyNWYzMWRhYzk4NDlkOTA2OWEKHwiE5aKzjgIQ2ruNtQYY7zEgDDCP5ZvPBTgCQPEHSAYaAmxmIiBkZjFlN2Q3Y2M4NmE1M2I0ZmY1ZmNiODJlMmFkNzZlNA; uid_tt=5f1caa6c2398c217970eb1c0888d421e; uid_tt_ss=5f1caa6c2398c217970eb1c0888d421e; sid_tt=a0b2a73b437e17bfd7a57a4f22fbeb63; sessionid=a0b2a73b437e17bfd7a57a4f22fbeb63; sessionid_ss=a0b2a73b437e17bfd7a57a4f22fbeb63; _bd_ticket_crypt_cookie=1159b093bada18097eac70c059ec032b; store-region=cn-fj; sid_guard=a0b2a73b437e17bfd7a57a4f22fbeb63%7C1724032196%7C5184000%7CFri%2C+18-Oct-2024+01%3A49%3A56+GMT; sid_ucp_v1=1.0.0-KDY4ODE4ZmIzOGU5MGU4MjAyNDFlNzhkNThlYzIzNWM2ZTM3ZDYzMDcKGQiE5aKzjgIQxMmKtgYY7zEgDDgCQPEHSAQaAmhsIiBhMGIyYTczYjQzN2UxN2JmZDdhNTdhNGYyMmZiZWI2Mw; ssid_ucp_v1=1.0.0-KDY4ODE4ZmIzOGU5MGU4MjAyNDFlNzhkNThlYzIzNWM2ZTM3ZDYzMDcKGQiE5aKzjgIQxMmKtgYY7zEgDDgCQPEHSAQaAmhsIiBhMGIyYTczYjQzN2UxN2JmZDdhNTdhNGYyMmZiZWI2Mw; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.99%7D; hevc_supported=true; SelfTabRedDotControl=%5B%5D; publish_badge_show_info=%220%2C0%2C0%2C1724665998709%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAQYcsLG7jTJVMpmh8J2leUv3IISG7pqgRRt4u5410kMk%2F1725033600000%2F0%2F0%2F1725004534150%22; strategyABtestKey=%221725259084.271%22; biz_trace_id=05e2740f; download_guide=%223%2F20240902%2F1%22; pwa2=%220%7C0%7C3%7C0%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAQYcsLG7jTJVMpmh8J2leUv3IISG7pqgRRt4u5410kMk%2F1725292800000%2F0%2F1725262014138%2F0%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRHl2R013UTNrNGI2NVJ3TjZPK2JCWU93WEpFdnlKajZub1pMeXBPZUtZbE1yOXFpQ0lOSXdSWU9uaHJ3TXVxc1BRQXNVTGNwazRoUlpvMU4vbUxyb1k9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; WallpaperGuide=%7B%22showTime%22%3A1723010509334%2C%22closeTime%22%3A1722568438498%2C%22showCount%22%3A6%2C%22cursor1%22%3A322%2C%22cursor2%22%3A7%2C%22hoverTime%22%3A1721202407527%7D; odin_tt=d1b0e0b39daa762b8646f4d569ea87541f782b4c5099b6de66837257740b08e7fc156e24b345af744cddafa1cb44a9eb; IsDouyinActive=false"
            #
            # }
            # rsp = requests.get(url1, headers=dy_header)
            # print(res.json())
            with open("C:\\Users\\admin\\Desktop\\161611565.txt", "r",encoding="utf-8") as f:
                text = f.read()
            data = json.loads(text)
            aweme_list = data['aweme_list']
            for aweme in aweme_list:
                video = aweme['video']
                aweme_id=aweme['aweme_id']
                play_addr = video['play_addr']
                play_url = play_addr['url_list'][0]
                if not os.path.exists(aweme_id + ".mp4"):
                    try:
                        self.oss.tqdm_download(aweme_id+ ".mp4",
                                           play_url)
                        if os.path.exists(aweme_id + ".mp4"):
                            shutil.copy(aweme_id + ".mp4", '//192.168.0.159/策划部视频共享池/开头吸晴')
                    except Exception as e:
                        print(e)
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
dy.postData()

# oss = aliyun_oss_comment.OssService()
# oss.tqdm_download("22222.mp4",
#                                  "http://v95-web-sz.douyinvod.com/37ea034a68b7744b6994a7a9aad81114/66bd8bce/video/tos/cn/tos-cn-ve-51/oYty07mXBnz7DcFhtYfDoI1ggLO3EQABjLQhnA/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=4034&bt=4034&cs=0&ds=4&ft=GZnU0RqeffPdXP~ka1jNvAq-antLjrKazVl.Rka~izvzljVhWL6&mime_type=video_mp4&qs=0&rc=NTo7NTY0ZWZlZGQ7ZGQ2NEBpajpxNnE5cmk5cTMzNDYzM0A0YmEzXjIyXzAxXzUyNS9iYSNmbWAyMmRzXmJgLS1kMC9zcw%3D%3D&btag=c0000e00018000&cquery=100B_102v_102u_100o_100w&dy_q=1723687296&feature_id=59cb2766d89ae6284516c6a254e9fb61&l=20240815100136CAD9A137F6BA0354BB57")