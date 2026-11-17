import time
import time
import sys
sys.path.append('../')
import time
from datetime import datetime
from urllib.parse import urlencode

import execjs
import requests
from bs4 import BeautifulSoup

import os


from sentiment import aliyun_oss_comment
#
from openai import OpenAI

from utils import Config

#
# client = OpenAI(
#         api_key="sk-x0cwou7m3dR3TNwwvrsAC0IxroUweWgyMMRsqAwqrrBBKLcM",
#         base_url="https://api.moonshot.cn/v1",
# )
# #
# history = [
#         {"role": "system",
#          "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
# ]
#
#
# def chat(query, history):
#         history += [{
#                 "role": "user",
#                 "content": query
#         }]
#         print(history)
#         completion = client.chat.completions.create(
#                 model="moonshot-v1-128k",
#                 messages=history,
#                 temperature=0.3,
#         )
#         result = completion.choices[0].message.content
#         history += [{
#                 "role": "assistant",
#                 "content": result
#         }]
#         return result
#
#
# index=0
#
# list=["地球的自转周期是多少?","月球呢？","两个星球自转有什么差别"]
#
# def job():
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         print(chat("地球的自转周期是多少？", history))
#         print("这是一个定时任务,更新时间为:" + current_time)
#
#         # 每隔5分钟运行一次job函数
#
#
# def run():
#         schedule.every(1).minutes.do(job)
#
#         while True:
#                 # 等待1秒钟
#                 time.sleep(1)
#                 # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
#                 schedule.run_pending()

# oss = aliyun_oss_comment.OssService()
# for i in range(1000):
#     oss.tqdm_download("recording_20240331045247-"+str(i)+".ts", "https://p2.bdstatic.com/rtmp.liveshow.lss-user.baidubce.com/live/stream_bduid_2014552507_9116683806/recording_20240331045247/recording_20240331045247-"+str(i)+".ts")


# Authorization: Bearer


# print(chat("月球呢？", history))
# from src.utils import Config, Proxie
# from src.utils.HttpUtil import HttpUtils
#
#
#
# #百家号
# r = requests.get("https://m.lawtime.cn/ask/question_33358453.html", headers=Config.weibo_headers, allow_redirects=False)
# print(r.text)
# print(r.content)
# real_url = r.headers.get('Location')
# print(real_url)
# res=requests.get(real_url, headers=headers, allow_redirects=False)
# print(res.text)
# soup = BeautifulSoup(r.text, "html.parser")
# container = soup.find('div', {'class': '_1HGmt'})
# a=container.find('a')
# print(a['href'])
# print(a.text)

# class VideoScraccy:
#     proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
#
#
#     def getuserId(self, sec_uid, cursor):
#         try:
#             proxy = Proxie.Proxie()
#             response1 = proxy.getProxie()
#             self.proxles['http'] = 'http://' + response1
#             self.proxles['https'] = 'http://' + response1
#             dy_header = Config.dy_header
#             param = {
#                 "device_platform": "webapp",
#                 "aid": "6383",
#                 "channel": "channel_pc_web",
#                 "sec_user_id": sec_uid,
#                 "max_cursor": cursor,
#                 "locate_query": "false",
#                 "show_live_replay_strategy": "1",
#                 "count": "20",
#                 "publish_video_strategy_type": "2",
#                 "pc_client_type": "1",
#                 "version_code": "170400",
#                 "version_name": "17.4.0",
#                 "cookie_enabled": "true",
#                 "screen_width": "1920",
#                 "screen_height": "1080",
#                 "browser_language": "zh-CN",
#                 "browser_platform": "Win32",
#                 "browser_name": "Chrome",
#                 "browser_version": "115.0.0.0",
#                 "browser_online": "true",
#                 "engine_name": "Blink",
#                 "engine_version": "115.0.0.0",
#                 "os_name": "Windows",
#                 "os_version": "10",
#                 "cpu_core_num": "4",
#                 "device_memory": "8",
#                 "platform": "PC",
#                 "downlink": "8.8",
#                 "effective_type": "4g",
#                 "round_trip_time": "0",
#                 "webid": "7224418331088242237"
#             }
#             xbogus = execjs.compile(open('D:\\gy\\py\\Sentiment\\dy_sign_news.js').read()).call('get_xb',
#                                                                                                 '/aweme/v1/web/aweme/post/?' + urlencode(
#                                                                                                     param))
#             print(xbogus)
#             r = requests.get("https://www.douyin.com" + xbogus, headers=dy_header, proxies=self.proxles)
#             print(r.text)
#
#             # has_more = data['has_more']
#             # max_cursor = data['max_cursor']
#             # aweme_list = data['aweme_list']
#             # array = []
#             # for aweme in aweme_list:
#             #     json_note = {}
#             #     json_note['platform'] = "抖音"
#             #     json_note['title'] = aweme['desc']
#             #     json_note['url'] = aweme['share_url']
#             #     json_note['account'] = aweme['author']['uid']
#             #     json_note['videoid'] = aweme['aweme_id']
#             #     array.append(json_note)
#             #     res = HttpUtils().sendGet("/api/get/my/video?aid=" + json_note['videoid'])
#             #     print(res.json())
#             #     if len(res.json()) > 0:
#             #         has_more = 0
#             #
#             # if has_more == 1:
#             #     self.getuserId(sec_uid, max_cursor)
#
#         except Exception as e:
#             print(e)
# #
# v=VideoScraccy()
# v.getuserId("MS4wLjABAAAA9WJqZgZIgTlX-1cvR2STbMLz2Rb9B_ESobIMQX9XfH-GOpmKgxrjAPqiTmqEopIB",0)

# dy_headers = Config.dy_header
# dy_headers['Referer']="https://www.douyin.com/video/7350308418147700002"
# dy_headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
# dy_headers['Accept']="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
# dy_headers['Cookie']="d_ticket=6812d18432bfda0d79a1185282dc7b36bb89e; xgplayer_user_id=147380391532; pwa2=%223%7C1%7C3%7C0%22; bd_ticket_guard_client_web_domain=2; odin_tt=a3b56745b632cab94eedffde59cb487000b839b5ddcbf5e85f227f15db16a174781300ba506f48b0271ea89acb691c955405d63a5b9fd74c77e935d479d09ecfc4639da241e245b5cc39856e1ba5214d; dy_swidth=1920; dy_sheight=1080; passport_csrf_token=7fce2c896374c6ad89c04cf90e886ebc; passport_csrf_token_default=7fce2c896374c6ad89c04cf90e886ebc; xgplayer_device_id=3165831672; ttwid=1%7Cl4EAJY9o-YR4Gg56ePtunuc1_ojwHxble6OqVenevVU%7C1710820535%7C3894537cc23dc190ae55e63cb3bdca9ec15c42890b24492034a9322900509fde; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; s_v_web_id=verify_lu2fe39x_08811f5a_050c_1fdb_e774_62a520fed222; csrf_session_id=c1cbb2215eb237bfc453957d722a36df; douyin.com; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.6%7D; SEARCH_RESULT_LIST_TYPE=%22single%22; download_guide=%223%2F20240408%2F0%22; GlobalGuideTimes=%221712630046%7C0%22; xg_device_score=6.09; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; strategyABtestKey=%221712798098.045%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCUDNBNDdyWENRc0J4V25GZGlHR2ZvaFZnUWorVmxvNkM3OW44THlHYUJLdVFVcGNzczF2ZzVIVm43ZDlwK3ZKMWoxOXpFdHZGWnJmT3RkNTVLNlVBc0k9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; __ac_nonce=066179762006fa44d19a9; __ac_signature=_02B4Z6wo00f01ppMg6wAAIDDkGpYBEJUKvqabIcAAMCQC2doyqimugsecEkx5C-6JLBxsHfbnKrBldlElh3ipvOesjcAXlCSPTDpP7m.e88ZjGPzH.HicKktMRAtLAqKKtgy0CeKS7NSAHugd2; msToken=b5d64VamqtrQVlsjNDZHIA5hMERq7frwIFYJ9z1eYwAtqe_0shjaX_t1lX1xgdTpDkAcwJS21I3NKz9qqgkT6O3vDIXqS2eeUzfOYJu5p7a-0UioEHBsT89RhQ89XoI=; tt_scid=2WgIqK-mv33SARXNzgB0uXgmSgwZXa3RlazCvekXQ9JQ55D6-hd.5Y5L2UvTc4kmfc17; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.75%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22"
# print("https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7350308418147700002&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=4&device_memory=8&platform=PC&downlink=1.65&effective_type=4g&round_trip_time=100&webid=7325254818271135251&msToken=wOzxnHkJTFbdgcepTYbhdthpmm_H1LQPpWMv2_juBtkSIB-7_J8fJ6YKLIlQWtcWYrT5I610eQhcon85dmg5UOjCTd1qhc6POHh2IURegNmClCPN_X3kO-VEMgNR83U=&X-Bogus=DFSzswVYhXJANnTJt501nTSX1b26")
# res3 = requests.get(url="https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7350308418147700002&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=4&device_memory=8&platform=PC&downlink=1.65&effective_type=4g&round_trip_time=100&webid=7325254818271135251&msToken=wOzxnHkJTFbdgcepTYbhdthpmm_H1LQPpWMv2_juBtkSIB-7_J8fJ6YKLIlQWtcWYrT5I610eQhcon85dmg5UOjCTd1qhc6POHh2IURegNmClCPN_X3kO-VEMgNR83U=&X-Bogus=DFSzswVYhXJANnTJt501nTSX1b26" , headers=dy_headers)
# print(res3.text)
#
# xhs_client = XhsClient(Config.xhs_Cookie)
# r = xhs_client.get_user_info("613821f6000000000201f39d")
# print(r)
# oss = aliyun_oss_comment.OssService()
# for i in range(1000):
#     oss.tqdm_download( "./temp/recording_20250416174641-"+str(i)+".mp4", "https://p2.bdstatic.com/rtmp.liveshow.lss-user.baidubce.com/live/stream_bduid_6794323689_10186582417/recording_20250416174641/recording_20250416174641-"+str(i)+".ts")
# folder_path="F:\\55"
# filenames = os.listdir(folder_path)
# for filename in filenames:
#     os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, filename.replace("美女_","")))
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import google.protobuf.message as message
def parse_key_from_json(self, json_file_path):
        """从io_data.json解析key_1"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 获取login_keys的base64值
            base64_str = data.get("login_keys", "")
            if not base64_str:
                raise ValueError("未找到login_keys字段")
            
            # Base64解码
            protobuf_bytes = base64.b64decode(base64_str)
            
            # Protobuf反序列化
            # 这里需要根据实际的protobuf结构来解析
            proto_msg = pb.LoginKeys()  # 假设的protobuf消息类
            proto_msg.ParseFromString(protobuf_bytes)
            
            # 获取key_1 - 这里需要根据实际protobuf结构调整
            key_1 = proto_msg.key_1  # 或通过相应字段获取
            return key_1
            
        except Exception as e:
            print(f"解析JSON文件失败: {e}")
            return None