import sys

import schedule
sys.path.append('../../')
import random
import time
from urllib.parse import urlencode

import execjs
import requests

from sentiment import aliyun_oss_comment
from utils.common_utils import CommonUtils
from datetime import datetime


class DyCommet:
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    oss = aliyun_oss_comment.OssService()
    count=3
    common_utils = CommonUtils()

    def getSendData(self, array, platform, analysis):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        return dd

    def getcomment(self, aweme_id, page,taskid):
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
            "Cookie": "bd_ticket_guard_client_web_domain=2; xgplayer_user_id=384125271196; UIFID_TEMP=29d6bea3e5a6c157a08a212e1912b5e8a78666ece26be56100fa19e58a63a45b18e84b3c21d3f0f2b0f9ecc0aa58a67b1a248997f136535c26be30cf2ecff98ae546654ac99fe76365c79f7cb3994507; fpk1=U2FsdGVkX19At8H8MoEcEjBANcv4c2h5DAKG9FzNh0V0xrma8ivsdoPjAnx50uUK+6/nxS1k3zKrg5Sv6dsSZA==; fpk2=c92baae71318dc81de51a663df2f8b4f; UIFID=29d6bea3e5a6c157a08a212e1912b5e8a78666ece26be56100fa19e58a63a45b6eec83a382132c2e52db5f2690dac763acd13c00f881883c0ee0d84769895280113c48b2ee54218bc6d2b6f820feadbf9e5ade60a74f69134df9ceda19bc10d0aa769c11c7c2ea29ebfbe11fb48b8053d2e8129ce35a13edeb972fea2a54bf4c40117ac3b23185f815705c6d4ed5770d4e9daa72f124e1ead5e71b1987219689; store-region-src=uid; my_rd=2; xgplayer_device_id=35696942262; hevc_supported=true; SelfTabRedDotControl=%5B%5D; store-region=cn-fj; live_use_vvc=%22false%22; volume_info=%7B%22isMute%22%3Afalse%2C%22volume%22%3A0.532%2C%22isUserMute%22%3Afalse%7D; __security_mc_1_s_sdk_sign_data_key_sso=ce919709-4c3e-818a; __security_mc_1_s_sdk_crypt_sdk=2fd58483-4566-a96a; ttwid=1%7C-xB26QX9XO-NyMtLpqWEQebBdw76v1LtUPysL_PPBAk%7C1741137884%7C6ed3ef0b4e9e42a6876af179424af1f8b291b970f776b0bb85c8704b79c7ceb7; x-web-secsdk-uid=34f359f0-ca67-4979-babb-fb7428615699; dy_swidth=1920; dy_sheight=1080; passport_csrf_token=00f8d309704e6d00247ff41d6fb22506; passport_csrf_token_default=00f8d309704e6d00247ff41d6fb22506; douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; is_dash_user=1; passport_mfa_token=Cjj8rMksUYljI2%2F9frEhwTe32HkDvbz4TIYccaCH4IVRvTTZ%2BslY6pUqHCGQXVflHW9DnLB7Q2iQ1RpKCjwAAAAAAAAAAAAATs%2BP3qgRhTYd%2FCCBZqDIxK%2BC344WlUD5y5h9z%2FMtOtb%2FnlXsrNTLGWEVgpdyjJ8t%2B4QQyJntDRj2sdFsIAIiAQMNPbVc; d_ticket=218ff84328fb5cb2188f5b1687ce79f6b3266; passport_assist_user=CkSEMeNK4fGGjFLF9Dl1ti_AEIicOofsVHqpPuR6Z7hbj8xigLnPwfc4TLI0NUi6UgUTwvh-24xJJuCGJTFcgAUJ37JdTBpKCjwAAAAAAAAAAAAATs_coBWe2DxIleM-BAHRfTdTFK0AmHr6R38pIa5NyP0NAyh_DBMj2VwFHhE1BHuUcYUQxZntDRiJr9ZUIAEiAQNdp8Jq; n_mh=IUC4d6dPpSphIM8MnFf8kA_66-ZjEWYAk3mP6_oovHk; sid_guard=0639d6263176c1d90d37c926852f0df3%7C1743132888%7C5184000%7CTue%2C+27-May-2025+03%3A34%3A48+GMT; uid_tt=0dc83ae3b5234063a9a4dc9b1442cb680d36c4e3e3e8830e60a6b4943922a5bb; uid_tt_ss=0dc83ae3b5234063a9a4dc9b1442cb680d36c4e3e3e8830e60a6b4943922a5bb; sid_tt=0639d6263176c1d90d37c926852f0df3; sessionid=0639d6263176c1d90d37c926852f0df3; sessionid_ss=0639d6263176c1d90d37c926852f0df3; is_staff_user=false; sid_ucp_v1=1.0.0-KGViYWUwODExZTU1MzFmMjgzZTQxY2Y3Nzc5NDgwOWM5MzE4OTAwYjcKIgi5iL3IrPCE82cQ2LGYvwYY7zEgDDDHsJi_BjgHQPQHSAQaAmxmIiAwNjM5ZDYyNjMxNzZjMWQ5MGQzN2M5MjY4NTJmMGRmMw; ssid_ucp_v1=1.0.0-KGViYWUwODExZTU1MzFmMjgzZTQxY2Y3Nzc5NDgwOWM5MzE4OTAwYjcKIgi5iL3IrPCE82cQ2LGYvwYY7zEgDDDHsJi_BjgHQPQHSAQaAmxmIiAwNjM5ZDYyNjMxNzZjMWQ5MGQzN2M5MjY4NTJmMGRmMw; login_time=1743132889806; _bd_ticket_crypt_cookie=221ca093b6aaa79a84b06c57e323b11f; __security_mc_1_s_sdk_sign_data_key_web_protect=0480932d-425c-8f7e; __security_mc_1_s_sdk_cert_key=b7cc0e1f-4acc-8c54; __security_server_data_status=1; xg_device_score=7.69985647220583; SearchMultiColumnLandingAbVer=1; SEARCH_RESULT_LIST_TYPE=%22multi%22; SearchSingleColumnExitCount=0; csrf_session_id=424c736d9a578fe35ddfe6485451898d; download_guide=%223%2F20250328%2F1%22; __ac_nonce=067f347a1009f840b70e6; __ac_signature=_02B4Z6wo00f01Vz9kfQAAIDBa9lVqwuaeNVc3ZVAADDP51; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; strategyABtestKey=%221743996836.462%22; s_v_web_id=verify_m96iore1_vLnBWu7i_CmVN_4bsC_8y7Y_opaegtCU592v; biz_trace_id=d00bb464; publish_badge_show_info=%220%2C0%2C0%2C1743996837630%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCREhjR0FmbysyNExEeUJEdWM0Um13bSt6UjNBUGMwcUdIbStwOHFDYzBFM1dWQzVtZjZEYU8xQytoL2owRFpoVHk2elRoNTRhTmNBYnc3eDVWenJrR289IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; odin_tt=7de3730e75366e4a121e5bcd75af1b3fe775634786e9c75cf2071537736378691f886d57694531ef2d9083025e8a40f1e489404d5f76c9fcbd40685a027ac3b1; passport_fe_beating_status=true; WallpaperGuide=%7B%22showTime%22%3A1743996863491%2C%22closeTime%22%3A0%2C%22showCount%22%3A2%2C%22cursor1%22%3A16%2C%22cursor2%22%3A4%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; IsDouyinActive=true"
        }
        comment_lsit_req_url = f"https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&cursor={str(page)}&count=10&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=134.0.0.0&browser_online=true&engine_name=Blink&engine_version=134.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7457730178169832972"
        abogus = self.common_utils.get_abogus(comment_lsit_req_url,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
        # url = "/aweme/v1/web/comment/list/?" + urlencode(param)
        # print(url)
        url = comment_lsit_req_url + "&a_bogus=" + abogus
        # "https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAALl94NtZS_4MdFPYlYWCcYImdL2x3hMDFMvV7sgu2NOg&max_cursor=0&locate_query=false&show_live_replay_strategy=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=115.0.0.0&browser_online=true&engine_name=Blink&engine_version=115.0.0.0&os_name=Windows&os_version=10&cpu_core_num=4&device_memory=8&platform=PC&downlink=8.8&effective_type=4g&round_trip_time=0&webid=7224418331088242237&msToken=ElUXIzqWoRlpDJ8OAaJj0mo3itWz8QIYHIZnkKvK1MJ8OwlGWwZxVhK7DNlBa4eXRczQyxF0eSvUHPoI4DXmqLBuGX6NKTQ06nRLN0mnA1g&X-Bogus=DFSzsrVOdy2ANnlKt9k2wVXAIQRU",
        r = requests.get(
            url,
            headers=dy_header)
        print(r.text+"----------------")
        content = r.json()
        has_more = content['has_more']
        comments = content['comments']
        array = []
        if comments is not None:
            for item in comments:
                jj = {}
                jj['taskId']=taskid
                if page==0:
                    jj['commentSort'] = 1
                else:
                    jj['commentSort'] = 2
                jj['platform'] = "抖音"
                jj['videoid'] = item['aweme_id']
                jj['comment_id'] = item['cid']
                if 'nickname' in item['user']:
                    jj['nickname'] = item['user']['nickname']
                else:
                    jj['nickname'] = item['user']['uid']
                jj['content'] = item['text']
                jj['comment_time'] = item['create_time']
                array.append(jj)
        if len(array):
            rt = requests.post("http://webstt.jiangxisls.com/api/postTaskComment",
                                   json=self.getSendData(array, "抖音", False))
            print(rt.text)

       

    def generate_random_str(self, randomlength=107):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def run(self):
        res = requests.get("http://webstt.jiangxisls.com/api/getCompleteTask?platform=1")
        print(res.text)
        aw = res.json()
        if len(aw) > 0:
            # try:
                self.getcomment(aw[0]['url'], 0,aw[0]['id'])
            # except Exception:
            #     print("错误了")
       
    def job(self):
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("这是一个定时任务,更新时间为:" + current_time)
            self.run()
        except Exception:
            print("错误了")

        # 每隔5分钟运行一次job函数
    def run1(self):
        schedule.every(10).minutes.do(self.job)
        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()

dycomment = DyCommet()
dycomment.run1()


