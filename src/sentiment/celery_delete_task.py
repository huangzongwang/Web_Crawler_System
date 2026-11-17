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
            "Cookie": "enter_pc_once=1; UIFID_TEMP=8f584679f13361d7674396b25a46f1c75dd7736730eef2bca7f1b3cfea8b216dd4980ee2672b358309640621d798c48491ba1457ca54c99ef4543dec626b28318680beb8f8e092d923786ddb689bc9ed; s_v_web_id=verify_mbuf8qfo_YmKrscWg_lxPw_4ZCe_8LMj_txPGCLryegbX; dy_swidth=1920; dy_sheight=1080; fpk1=U2FsdGVkX1+25BUQulllV78ZCdUXm06p+9wJb1YvrVcIGFc1eDC0uObtSf6JP9N92G7LBSMD7fUqsQN1NBdv7A==; fpk2=8cf04e281318af421dc03fc482e00bfd; xgplayer_user_id=705019309323; passport_csrf_token=ff2762b54dfc6f8a1b9f0cc5b318511c; passport_csrf_token_default=ff2762b54dfc6f8a1b9f0cc5b318511c; __security_mc_1_s_sdk_crypt_sdk=8ca19e11-4340-85a7; __security_mc_1_s_sdk_cert_key=5f347b9a-460c-92f3; bd_ticket_guard_client_web_domain=2; UIFID=8f584679f13361d7674396b25a46f1c75dd7736730eef2bca7f1b3cfea8b216d4e9949dbc792f6e111a402c49ffb0868ad12faf3a12f394ed4346968545c2071ddb713be1704171f479ec65419b151d63069baa5d66fce8715c7f2b944ebac44814094350b8be6f2a0d0834a2d7c8a56520f931f57e74403703f2caef7f4354d4f8a969e96592e5655fab2e54f9f66aff716d1a9da7d062b09b06cd1221d9893; passport_auth_status=999d29e3c8ab7707c73cac4b86b454dd%2C; passport_auth_status_ss=999d29e3c8ab7707c73cac4b86b454dd%2C; is_staff_user=false; SelfTabRedDotControl=%5B%5D; __security_server_data_status=1; xgplayer_device_id=67598820784; live_use_vvc=%22false%22; _bd_ticket_crypt_doamin=2; SEARCH_RESULT_LIST_TYPE=%22single%22; volume_info=%7B%22volume%22%3A0.138%2C%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%7D; __druidClientInfo=JTdCJTIyY2xpZW50V2lkdGglMjIlM0EyOTglMkMlMjJjbGllbnRIZWlnaHQlMjIlM0E2OTQlMkMlMjJ3aWR0aCUyMiUzQTI5OCUyQyUyMmhlaWdodCUyMiUzQTY5NCUyQyUyMmRldmljZVBpeGVsUmF0aW8lMjIlM0EwLjc1JTJDJTIydXNlckFnZW50JTIyJTNBJTIyTW96aWxsYSUyRjUuMCUyMChXaW5kb3dzJTIwTlQlMjAxMC4wJTNCJTIwV2luNjQlM0IlMjB4NjQpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGMTM4LjAuMC4wJTIwU2FmYXJpJTJGNTM3LjM2JTIwRWRnJTJGMTM4LjAuMC4wJTIyJTdE; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; publish_badge_show_info=%221%2C0%2C0%2C1752111575829%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA3pZnOeC9Q18Ji2_DvhMcO2QJbfbrQwLVOF2nAbzWwP4%2F1752163200000%2F0%2F0%2F1752132541951%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA3pZnOeC9Q18Ji2_DvhMcO2QJbfbrQwLVOF2nAbzWwP4%2F1752163200000%2F0%2F1752134774964%2F0%22; download_guide=%223%2F20250710%2F0%22; passport_mfa_token=CjjwsN5Jul08xQKD%2FSiwVqUOQJDUQWIwtSgdXdBRy3b%2B%2F8C84Jj2FM7ShmuA607zx7%2FN8wyDoHohwRpKCjwAAAAAAAAAAAAATze3TvqIC0GY7KoVy2iz%2BgkCbnEgd4jBy1BfNBB9nFqp1KsTe5H3Y5u7PBsiLf0BfkgQl672DRj2sdFsIAIiAQOvRMlc; d_ticket=fa9a5bc260c582c61feb348fac8df893423d6; passport_assist_user=CkQfhlSglGhCDxsMZgEEyNPawfr5GMVX1cECWMTFZer4wgvuNTpuAoNYKUCzftjORgPU0f9ePIdLfd0SuiJAOL2urscAaBpKCjwAAAAAAAAAAAAATzcYIPMqpvtaAH2f42l8dcu9ErYUwwYALzEFmq5qUj_NX3HrLPTGXjOSDJN8EOIhdq0Qtqz2DRiJr9ZUIAEiAQO48kLH; n_mh=ti0Yom2SdZI5mLQK8fAEyJH_Jgu_AIE0ocOw5dV5BwM; sid_guard=5c09ab327c19f1028c34a8d477418827%7C1752134950%7C5184000%7CMon%2C+08-Sep-2025+08%3A09%3A10+GMT; uid_tt=afd2834aa87f126c789791854b7972fb99c868418de912160dc228f5b485c755; uid_tt_ss=afd2834aa87f126c789791854b7972fb99c868418de912160dc228f5b485c755; sid_tt=5c09ab327c19f1028c34a8d477418827; sessionid=5c09ab327c19f1028c34a8d477418827; sessionid_ss=5c09ab327c19f1028c34a8d477418827; session_tlb_tag=sttt%7C12%7CXAmrMnwZ8QKMNKjUd0GIJ__________HrD7SMxtdxE0z5kBUHG9cgANsr251XQClyswBSU0De1g%3D; sid_ucp_v1=1.0.0-KDg3ZTQ1ZjkzOGEyNjhmYTQxMGIzZDI0NGY1ZDU0NThhMzRkNTlhNTcKIgi7iJWWhtTct2gQpuq9wwYY7zEgDDDC6L3DBjgHQPQHSAQaAmxxIiA1YzA5YWIzMjdjMTlmMTAyOGMzNGE4ZDQ3NzQxODgyNw; ssid_ucp_v1=1.0.0-KDg3ZTQ1ZjkzOGEyNjhmYTQxMGIzZDI0NGY1ZDU0NThhMzRkNTlhNTcKIgi7iJWWhtTct2gQpuq9wwYY7zEgDDDC6L3DBjgHQPQHSAQaAmxxIiA1YzA5YWIzMjdjMTlmMTAyOGMzNGE4ZDQ3NzQxODgyNw; login_time=1752134954079; _bd_ticket_crypt_cookie=6a2a3c19ebb4e8643e15fe0b8c5b6997; __security_mc_1_s_sdk_sign_data_key_web_protect=f5d709ee-42ed-8b61; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; strategyABtestKey=%221752194275.809%22; passport_fe_beating_status=true; csrf_session_id=dd6b9aa8b78efc15282f87fd49d7d8f4; __ac_nonce=06870896c00e475d2d2b4; __ac_signature=_02B4Z6wo00f01mJloFAAAIDCVUFkDL6Hao5iRaTAAPD4a8; biz_trace_id=4b51f03a; WallpaperGuide=%7B%22showTime%22%3A1751341920068%2C%22closeTime%22%3A0%2C%22showCount%22%3A6%2C%22cursor1%22%3A128%2C%22cursor2%22%3A40%2C%22hoverTime%22%3A1749795917039%7D; xg_device_score=7.670463056025158; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTWpQeTlsNHBtb2dLUTJJbUlLZEp2K3ZDWndDZ0JMdE5pR2pHNkNlNGNhcVVQRUdLa1Q3WnFHNkxucXdLYWZhVzJsVHh5MCsxcmRDSVRDbnVPMDQrMlU9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; ttwid=1%7CJfAJLOo6h-Y6NGYCGfzMq-WiHdasFWPiRHkt_KAQxtI%7C1752205871%7C365fa2c2de041741e4295d5ff731978e30906712a09bc04c76b28ec17924887b; odin_tt=ad7956068edc4ff47b522cab3ace6a792d9dbe43d784cf0d58d5d58135527bb2c294bc05af83ef1f062d8cebedefa424c03825f4ce5913e0d6b28608dd84d9afd88a8906d8610e3a70c3c6939c701246; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A1%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22"
        }
        comment_lsit_req_url = f"https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&cursor={str(page)}&count=10&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=134.0.0.0&browser_online=true&engine_name=Blink&engine_version=134.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7457730178169832972"
        abogus = self.common_utils.get_abogus(comment_lsit_req_url,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
        url = comment_lsit_req_url + "&a_bogus=" + abogus
        r = requests.get(
            url,
            headers=dy_header)
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
            "type":type1
        }
        if brand == "快手":
            res = requests.get("https://www.kuaishou.com/short-video/" + mid, headers=tyc_header)
            res = requests.get(res.url, headers=Config.ks_header)
            real_url = res.headers.get('Location')
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
                if has_Air:
                    print("抖音已经被删除")
                    data['isShield']=2
                res = HttpUtils().sendPost1(data, "/api/postSentimentContent")
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

    def run3(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("======================================"+current_time)
        try:
            dd=['快手','百度','搜狗','抖音']
            for d in dd:
                print({"platform":d,"isShield":0})
                respone = HttpUtils().sendPost1(json={"platform":d,"isShield":0},url="/api/getSentimentList")
                print(respone.text)
                if len(respone.json())>0:
                    self.run(d, respone.json()[0]['mid'],respone.json()[0]['url'],5)
        except Exception:
            print("错误了")
                    
    def run4(self):
        schedule.every(2).minutes.do(self.run3)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()

dyvideo = DeleteTask()
# dyvideo.run("抖音", "6499233092018913806","https://www.douyin.com/video/6499233092018913806")
# dyvideo.run2()
dyvideo.run4()
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
