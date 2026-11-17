import sys
sys.path.append('../')
import json
import time
from urllib import parse
from urllib.parse import urlencode
from utils.common_utils import CommonUtils

import execjs
import requests
from bs4 import BeautifulSoup
from xhs import XhsClient

from utils import Config
from utils.HttpUtil import HttpUtils

from utils import Proxie
import schedule
from datetime import datetime


class DeleteTask:
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    # chrome_options = Options()
    # # chrome_options.add_argument(
    # #     '--proxy-server={}:{}'.format(response1.split(":")[0], response1.split(":")[1]))
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # # chrome浏览器文件路径
    # # 创建浏览器对象
    # browser = webdriver.Chrome(options=chrome_options)
    # browser.get("https://www.baidu.com/")
    # window_handl = browser.current_window_handle
    common_utils = CommonUtils()

    def chuli(self, d):
        key = ""
        list = []  # 用于存储字典中的键值对,元素为元组
        for i in d.items():  # 以元组的格式读取键值对
            list.append(i)  # 将遍历到的元组加入列表中
        for num in range(len(list)):  # 遍历列表中的元组格式的键值对
            if len(list[num][0]) == 32:
                key = list[num][0]
        return key
    
    def getcomment(self, aweme_id, page):
        print(aweme_id+"-----------------------")
        dy_header = {
            "Host": "www.douyin.com",
            "Connection": "keep-alive",
            "sec-ch-ua": "Not.A/Brand;v=8, Chromium;v=114, Google Chrome;v=115",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.douyin.com/search/%E8%B5%9B%E4%B9%90%E8%B5%9B%E9%AA%97%E5%B1%80?aid=f5fc1d6c-eff4-4975-8148-c32edbc598d8&aweme_id=6747115414725168398&enter_from=video_detail&gid=6747115414725168398&source=search_history",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie":"UIFID_TEMP=630dc87f7218843564944b22829d362b9fabe9a9e3376a5c74988083749b66df2b8ba5909a6d457e74b30b6b2f7ee79027c43d9f4429538b75078c35f493877a826b36694fa12c0103e298b11a6b9d93; hevc_supported=true; xgplayer_user_id=280813430672; bd_ticket_guard_client_web_domain=2; fpk1=U2FsdGVkX1/N+SGEpw8Ru9f1/RyXM3HPyAMg4DD8a2lCc3bq04Fc4q5vZNO1f+68D5C0STdk8vVHedIVDCIH4A==; fpk2=4f09e01c83d69100c363c33aecfef9f8; UIFID=630dc87f7218843564944b22829d362b9fabe9a9e3376a5c74988083749b66df8003cd055ab5e06b23c0644e766a10de38629366b1c08e9fe873a4ea7e1dd7d2f8e9acccdb3ac994262d71986b5b7400b454a446c0f6917df738f41f4f4b1d05ae2eb388bcd4d238db09f43813fc570c685e89b1d660b7099d2da1912119cb9c7a4f2e7877877eb7a2aeb237f9d24578d0b8f01ea72841c6e43b02b348e5f06c; is_dash_user=1; __security_server_data_status=1; SearchMultiColumnLandingAbVer=1; SEARCH_RESULT_LIST_TYPE=%22multi%22; xgplayer_device_id=52593508643; MONITOR_WEB_ID=ac1aff1b-1c6b-4184-b4ec-effeddfdaf1a; is_staff_user=false; dy_swidth=1920; dy_sheight=1080; s_v_web_id=verify_mb68vcwx_9lues9GK_Xsoo_4JSW_97W6_C0xsliZDzVCK; __security_mc_1_s_sdk_crypt_sdk=90101bf2-488f-913f; passport_csrf_token=dddf8281947683d6c5935802ede6db83; passport_csrf_token_default=dddf8281947683d6c5935802ede6db83; enter_pc_once=1; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.11%7D; my_rd=2; login_time=1749786838433; passport_mfa_token=Cjd9X%2BQQEk%2Fd1KqqLgkCBGLR4RsBUJA4q3T%2Fil2mA7mv18WcAcwSCXa%2FR0CF%2Brtqhe2wZNFAPwlpGkoKPAAAAAAAAAAAAABPHJgeesT%2Fwnf3EDJNvhnahH2BgCo91lusarzm7IwQeDk5uF6rlvTDELx5RWtt8BROQxDD%2FfMNGPax0WwgAiIBA6wj7fg%3D; d_ticket=1a8ac7045693167dbf7590240665ea98da42a; passport_assist_user=CkE6NDHOIlS37G6OFMChocpT4QD74aRr2gyCl5RBzIZzqfY0nEKPm4UgCGxQsDA6C9h1hmSrEAvzldXo4cc1wA4d9BpKCjwAAAAAAAAAAAAATxzayyvRvnKzunrUF4Zx3aBBMJ_EeZOXYQmXWLeAZJ-MStNzH_2_ZVMQygKl0ZAvhFoQgvzzDRiJr9ZUIAEiAQMFSA_I; n_mh=R-jASNZLCmGIvGiWu-unAuYtHT9RDkwZcdp1r4Wu474; sso_uid_tt=93eda01cef7e5e73ce03fb68b645fe74; sso_uid_tt_ss=93eda01cef7e5e73ce03fb68b645fe74; toutiao_sso_user=39649c42a7b511ad0498e79f00937219; toutiao_sso_user_ss=39649c42a7b511ad0498e79f00937219; sid_ucp_sso_v1=1.0.0-KGQ1MWQxYmVlNGEyODRiNzlhMTc3MTM2ZGFiM2U5MWI2OTk0MjFlYjcKIQiJgtChkKzgBBD4gK_CBhjvMSAMMNeGwcAGOAZA9AdIBhoCbGYiIDM5NjQ5YzQyYTdiNTExYWQwNDk4ZTc5ZjAwOTM3MjE5; ssid_ucp_sso_v1=1.0.0-KGQ1MWQxYmVlNGEyODRiNzlhMTc3MTM2ZGFiM2U5MWI2OTk0MjFlYjcKIQiJgtChkKzgBBD4gK_CBhjvMSAMMNeGwcAGOAZA9AdIBhoCbGYiIDM5NjQ5YzQyYTdiNTExYWQwNDk4ZTc5ZjAwOTM3MjE5; __security_mc_1_s_sdk_sign_data_key_sso=1330d608-4174-b3b1; passport_auth_status=3ab926e8b85fca31ca306e3f2d514652%2C; passport_auth_status_ss=3ab926e8b85fca31ca306e3f2d514652%2C; uid_tt=9b4a0b2f29bac17ebe3273aa2be64cd3; uid_tt_ss=9b4a0b2f29bac17ebe3273aa2be64cd3; sid_tt=b7d19e6a5f1762b5ac9c7f0f1216256a; sessionid=b7d19e6a5f1762b5ac9c7f0f1216256a; sessionid_ss=b7d19e6a5f1762b5ac9c7f0f1216256a; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=dfe2a2b30e614730ad0f37f96a29e245; __security_mc_1_s_sdk_sign_data_key_web_protect=2f0f8b52-43ba-bdf7; SelfTabRedDotControl=%5B%5D; __security_mc_1_s_sdk_cert_key=429dbca7-4a0b-be94; session_tlb_tag=sttt%7C3%7Ct9Geal8XYrWsnH8PEhYlav_________Hjv2jemqXSkoJ7xAFKYUMX6PVQKkXence9Lnyh4UfYT4%3D; sid_guard=b7d19e6a5f1762b5ac9c7f0f1216256a%7C1752026059%7C5184000%7CSun%2C+07-Sep-2025+01%3A54%3A19+GMT; sid_ucp_v1=1.0.0-KGU0NTcyZjVhNjNlMzAzY2U2ZjFiZDZhOWFkM2E1MDIwNzJjOThmNTgKGwiJgtChkKzgBBDLl7fDBhjvMSAMOAZA9AdIBBoCbHEiIGI3ZDE5ZTZhNWYxNzYyYjVhYzljN2YwZjEyMTYyNTZh; ssid_ucp_v1=1.0.0-KGU0NTcyZjVhNjNlMzAzY2U2ZjFiZDZhOWFkM2E1MDIwNzJjOThmNTgKGwiJgtChkKzgBBDLl7fDBhjvMSAMOAZA9AdIBBoCbHEiIGI3ZDE5ZTZhNWYxNzYyYjVhYzljN2YwZjEyMTYyNTZh; publish_badge_show_info=%220%2C0%2C0%2C1752026062913%22; douyin.com; device_web_cpu_core=6; device_web_memory_size=8; architecture=amd64; xg_device_score=7.340468163808556; strategyABtestKey=%221752131246.343%22; biz_trace_id=9ed7254a; passport_fe_beating_status=true; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f273d333636353636363437303234272927676c715a75776a716a666a69273f2763646976602778; bit_env=YzWPD9s9SxeBUIjn_hVipikj8HsO-KbKaTXOerpXjB_V5L7twC803FCNTs1c0cm60sV_55i7WSlrb6c8by1h6IGB3HqmvI21l6knDaRYpvfGtJ4-eKuByht6bFXuqPcyoeALzylZUOTIV3gnb25igAgnQpQKCstEG_YL3wKhPXu3e1kpkWwJWm7rEjzqiBCmNr5HVKU6sJUWwpoQRDclyam76oR2c3czWLJb5zAOsJyuVLbpJIjYWznMNMzvr9Ay9TpPONnljvjb2rnbXbU0O4w__toF_vgo1Crfj_s5p34MWR9rOVYYApk5OWf_wqgHSdpj35QxGKa-e1qhUgfyYaU6VIio4M6UY-0bQRa29sOZ-334KslMy1tnOBjaoRX7IcOAdeJ_SshqU60nNrd7_fGN3xpQyjsQVsyIyvaX1I2bicjBPCm_8gPlBrvFaLm0DhcVSHzT3ug6hJVTWIoarwiKDIdzgRdKYJQ2_3wed5zGlEPPylD9BxMlxwE6iidC; gulu_source_res=eyJwX2luIjoiODhiMTRlZDdlNjhjYjQ0MzY4NWQ2M2E0OGRiYzljZDRiMDA5NGE0MWVjOWM1NTQ1YzEwODNhOGNiMjM3ZGI0MiJ9; passport_auth_mix_state=5oyjjed9ygt5mpr3sb2cpu3rnme4i3fe; __ac_nonce=0686f6ee6006f5f3a49d6; __ac_signature=_02B4Z6wo00f01hIRzjgAAIDDGDcVkhjsiKYSMcqAAOz5c4; ttwid=1%7CNq1aG6VNIrel5_EoaA41eVtOkxWLhvbKURbQlRpk1Ik%7C1752133357%7Cc4a357fcbb95c778b1e509c96b735ba2a0080da1096e1c1484cbc473829149b4; download_guide=%221%2F20250710%2F0%22; IsDouyinActive=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A6%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTm93dDRSRjYwTHpKM0VEZTVocml0VExiWkpOdG5UTHdYTFA5VzNwQjVBQld4UjNFT256NnF1VzljY2dZdUxGb2tDejNBN0tIaENtOWM5VjkvYUhNa3M9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; odin_tt=fbdd609f4b9cdd82dc522d0476a99afd6885b750ff2938b6e6363a63cc289ef7bb5655afdacc62838284e2cda1117bd6"
        }
        comment_lsit_req_url = f"https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&cursor={str(page)}&count=10&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=134.0.0.0&browser_online=true&engine_name=Blink&engine_version=134.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7457730178169832972"
        abogus = self.common_utils.get_abogus(comment_lsit_req_url,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
        url = comment_lsit_req_url + "&a_bogus=" + abogus
        print(url)
        r = requests.get(
            url,
            headers=dy_header)
        print(r.text)
        content = r.json()
        self.has_more = content['has_more']
        print(self.has_more)
        if "total" in content:
            return False
        else:
            return True
           

    def run(self, brand, mid,url,type1):
        # try:
        tyc_header = {
            "Connection": "keep-alive",
            "sec-ch-ua": "Google Chrome;v=113, Chromium;v=113, Not-A.Brand;v=24",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        data = {
            "mid": mid,
            "type":type1,
            "platform":brand
        }
        if brand == "快手":
            res = requests.get("https://www.kuaishou.com/short-video/" + mid, headers=tyc_header)
            res = requests.get(res.url, headers=Config.ks_header)
            if str(res.text).__contains__("作品已失效"):
                data['isShield']=2
            elif str(res.text).__contains__("无法连接网络"):
                data['isShield']=2
            res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
        elif brand == "微博":
            res = requests.get("https://weibo.com/ajax/statuses/show?id=" + mid + "&locale=zh-CN",
                               headers=tyc_header)
            if res.json()['message'] == "该微博不存在":
                data['isShield']=2
            elif res.json()['message'] == "由于博主设置，目前内容暂不可见。":
                data['isShield']=2
            res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
        elif brand == "抖音":
            try:
                has_Air=self.getcomment(mid,0)
                print(has_Air)
                if has_Air:
                    data['isShield']=2
                print(data)
                res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
                print(res.text)
            except Exception as e:
                res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
        elif brand == "百度":
            try:
                r = requests.get(url, headers=Config.dl_header,
                             allow_redirects=False)
                if str(r.text).__contains__("赛乐赛"):
                    data['isShield']=2
                elif str(r.text).__contains__("404"):
                    data['isShield']=2
                res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
            except Exception as e:
                data['isShield']=2
                res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
        elif brand == "搜狗":
            try:
                r = requests.get(url, headers=Config.dl_header,
                             allow_redirects=False)
                if str(r.text).__contains__("赛乐赛"):
                    data['isShield']=2
                elif str(r.text).__contains__("404"):
                    data['isShield']=2
                res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
            except Exception as e:
                data['isShield']=2
                res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
            
            

        # time.sleep(500)
        # self.run1()


    def run1(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("-----------------------"+current_time)
        try:
            dd=['快手','百度','搜狗','抖音']
            for d in dd:
                # print({"platform":d,"isShield":1})
                respone = HttpUtils().sendPost1(json={"platform":d,"isShield":1},url="/api/getSentimentList")
                print(respone.content)
                print(respone.text)
                print(respone.json())
                if len(respone.json()):
                    self.run(d, respone.json()[0]['mid'],respone.json()[0]['url'],4)
        except Exception as e:
            print("错误了")

                    
    def run2(self):
        schedule.every(3).minutes.do(self.run1)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()


dyvideo = DeleteTask()
# dyvideo.run("抖音", "6499233092018913806","https://www.douyin.com/video/6499233092018913806")
# dyvideo.getcomment("6499233092018913806",0)
dyvideo.run2()


# if __name__ == '__main__':
#     def food_video():
#         respone = HttpUtils().sendGet("/api/getNegativeList")
#         print(respone.text)
#         if len(respone.json()):
#             dyvideo = DeleteTask()
#             dyvideo.run(respone.json()[0]['platform'], respone.json()[0]['mid'], respone.json()[0]['videoType'])
#
#
#     scheduler = BlockingScheduler()
#     # # #
#     # # # # 添加任务
#     scheduler.add_job(food_video, 'interval', minutes=10)
#
#     scheduler.start()
