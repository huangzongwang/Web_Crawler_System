# -*- coding: utf-8 -*-

import requests
import subprocess

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def get_ab(url):
    p = subprocess.Popen(['node', './a_bogus',url], stdout=subprocess.PIPE)
    url = p.stdout.read().strip()
    return url


def get_comment_list(aweme_id,ttwid):
    url = f"https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&cursor=0&count=20&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=124.0.0.0&browser_online=true&engine_name=Blink&engine_version=124.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7361743797237679616"
    headers = {
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?0",
        "user-agent": userAgent,
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"https://www.douyin.com/?recommend=1",
        "cookie": f"ttwid={ttwid}; douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; home_can_add_dy_2_desktop=%220%22; dy_swidth=1920; dy_sheight=1080;",
        "Priority": "u=1, i"
    }
    url=f"https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&enable_history=1&keyword=%E8%B5%9B%E4%B9%90%E8%B5%9B%E5%87%8F%E8%82%A5%E5%8F%8D%E5%BC%B9%E4%B8%A5%E9%87%8D&search_source=search_history&query_correct_type=1&is_filter_search=0&from_group_id=&offset=0&count=10&need_filter_settings=0&search_id=20240528151351D62EC61004DB86084CB1&update_version_code=170400&pc_client_type=1&version_code=190600&version_name=19.6.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=125.0.0.0&browser_online=true&engine_name=Blink&engine_version=125.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7365729216689964583"
    url = get_ab(url)
    print(url)
    rest = requests.get(url,headers=headers).text
    return rest


def get_user_feed(sec_user_id,ttwid):
    url = f"https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={sec_user_id}&max_cursor=0&locate_item_id=7341406931216518412&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=124.0.0.0&browser_online=true&engine_name=Blink&engine_version=124.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50"
    headers = {
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?0",
        "user-agent": userAgent,
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"https://www.douyin.com/?recommend=1",
        "cookie": f"ttwid={ttwid}; douyin.com; device_web_cpu_core=20; device_web_memory_size=8; architecture=amd64; home_can_add_dy_2_desktop=%220%22; dy_swidth=1920; dy_sheight=1080;",
        "Priority": "u=1, i"
    }
    url = get_ab(url)
    print(url)
    rest = requests.get(url,headers=headers).text
    return rest


if __name__ == '__main__':
    sec_user_id = "MS4wLjABAAAAnZwyWcn9x8qLvF9sJNaO5iTSdXPQtXltUu6vR0YIAAI"
    # 复制个新的ttwid测试，用请求取一个也行
    # ttwid = "1%7CtIiOaT1adWsSj7Ul5R2BgGQzU5QDejOd8zu1wP2Ifh4%7C1714039561%7C09bfef0cba93646268923dec34c4fa6a2f0b336d794d64916232ef3986133b49"
    ttwid="1%7CdMXTb370DDbY28a99jMxErfatwow0GjGEjIa7HwkVlE%7C1716964071%7C6f67b8760dc98eb66fc09513951cf41beda123649161713e0a04ff7335267baf"
    comment_list = get_comment_list("7341406931216518412",ttwid)
    print(comment_list)
    # user_feed = get_user_feed(sec_user_id,ttwid)
    # print(user_feed)
