import time
from datetime import datetime

import execjs

import requests
import schedule

from src.sentiment import aliyun_oss_comment
from src.utils import Proxie, PhoneNumber, Config
from urllib.parse import urlencode
import urllib.parse

from src.utils.HttpUtil import HttpUtils


class DyTask():
    proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
    model_path = './data/bayes.pkl'
    userdict_path = './data/userdict.txt'
    stopword_path = './data/stopwords.txt'
    keyword=None

    def job(self):
        url = "http://webstt.jiangxisls.com/api/getkey?status=2"
        print(url)
        res = requests.get(url)
        if len(res.json())>0:
            dy_headers = Config.dy_header
            dy_headers[
                'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            dy_headers[
                'Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            dy_headers[
                'Cookie'] = "d_ticket=6812d18432bfda0d79a1185282dc7b36bb89e; xgplayer_user_id=147380391532; pwa2=%223%7C1%7C3%7C0%22; bd_ticket_guard_client_web_domain=2; odin_tt=a3b56745b632cab94eedffde59cb487000b839b5ddcbf5e85f227f15db16a174781300ba506f48b0271ea89acb691c955405d63a5b9fd74c77e935d479d09ecfc4639da241e245b5cc39856e1ba5214d; dy_swidth=1920; dy_sheight=1080; passport_csrf_token=7fce2c896374c6ad89c04cf90e886ebc; passport_csrf_token_default=7fce2c896374c6ad89c04cf90e886ebc; xgplayer_device_id=3165831672; ttwid=1%7Cl4EAJY9o-YR4Gg56ePtunuc1_ojwHxble6OqVenevVU%7C1710820535%7C3894537cc23dc190ae55e63cb3bdca9ec15c42890b24492034a9322900509fde; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; s_v_web_id=verify_lu2fe39x_08811f5a_050c_1fdb_e774_62a520fed222; csrf_session_id=c1cbb2215eb237bfc453957d722a36df; douyin.com; device_web_cpu_core=4; device_web_memory_size=8; architecture=amd64; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.6%7D; SEARCH_RESULT_LIST_TYPE=%22single%22; download_guide=%223%2F20240408%2F0%22; GlobalGuideTimes=%221712630046%7C0%22; xg_device_score=6.09; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; strategyABtestKey=%221712798098.045%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCUDNBNDdyWENRc0J4V25GZGlHR2ZvaFZnUWorVmxvNkM3OW44THlHYUJLdVFVcGNzczF2ZzVIVm43ZDlwK3ZKMWoxOXpFdHZGWnJmT3RkNTVLNlVBc0k9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; __ac_nonce=066179762006fa44d19a9; __ac_signature=_02B4Z6wo00f01ppMg6wAAIDDkGpYBEJUKvqabIcAAMCQC2doyqimugsecEkx5C-6JLBxsHfbnKrBldlElh3ipvOesjcAXlCSPTDpP7m.e88ZjGPzH.HicKktMRAtLAqKKtgy0CeKS7NSAHugd2; msToken=b5d64VamqtrQVlsjNDZHIA5hMERq7frwIFYJ9z1eYwAtqe_0shjaX_t1lX1xgdTpDkAcwJS21I3NKz9qqgkT6O3vDIXqS2eeUzfOYJu5p7a-0UioEHBsT89RhQ89XoI=; tt_scid=2WgIqK-mv33SARXNzgB0uXgmSgwZXa3RlazCvekXQ9JQ55D6-hd.5Y5L2UvTc4kmfc17; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.75%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22"
            print(
                "https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7350308418147700002&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=4&device_memory=8&platform=PC&downlink=1.65&effective_type=4g&round_trip_time=100&webid=7325254818271135251&msToken=wOzxnHkJTFbdgcepTYbhdthpmm_H1LQPpWMv2_juBtkSIB-7_J8fJ6YKLIlQWtcWYrT5I610eQhcon85dmg5UOjCTd1qhc6POHh2IURegNmClCPN_X3kO-VEMgNR83U=&X-Bogus=DFSzswVYhXJANnTJt501nTSX1b26")
            dy_headers['Referer']="https://www.douyin.com/video/"+res.json()[0]['videoid']
            print("https://www.douyin.com"+res.json()[0]['url'])
            res3=requests.get(url=res.json()[0]['url'],headers=dy_headers)
            print(res3.text)
            if res3.json()['aweme_detail']==None:
                data = {
                    "mid": res.json()[0]['videoid']
                }
                res1 = HttpUtils().sendPost(data, "赛乐赛", "/api/updateSubjectStatus", False)
                print(res1.text)
                res2 = HttpUtils().sendPost1(json={"videoid": res.json()[0]['videoid'], "status": 3}, url="/api/postupdatekey")
                print(res2.text)




    # 每隔5分钟运行一次job函数
    def run(self):
        schedule.every(5).minutes.do(self.job)

        while True:
            # 等待1秒钟
            time.sleep(1)
            # 如果当前时间到达了设定的定时任务时间点，则调用对应的函数
            schedule.run_pending()




dy=DyTask()
# dy.getIp()
dy.run()

