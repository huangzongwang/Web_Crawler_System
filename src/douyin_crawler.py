

"""
    抖音评论爬取
"""
from utils.Proxie import Proxie
from utils.common_utils import CommonUtils
import copy
import json

import requests
from urllib.parse import urlparse, parse_qs
from urllib.parse import quote
from utils import Config

class DyComment:

    def __init__(self):

        self.common_utils = CommonUtils()
        self.comment_list_headers = {
            'sec-ch-ua':'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Accept':'application/json, text/plain, */*',
            'sec-ch-ua-mobile':'?0',
            'User-Agent':self.common_utils.user_agent,
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Dest':'empty',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def get_comment_list(self, aweme_id):
        # if ('modal_id' in req_url):
        #     aweme_id = parse_qs(urlparse(req_url).query).get('modal_id')[0]
        # else:
        #     aweme_id = urlparse(req_url).path.split("/")[-1]
        referer_url = f"https://www.douyin.com/discover?modal_id={aweme_id}"
        ms_token = self.common_utils.get_ms_token()
        ttwid_str, webid = self.common_utils.get_ttwid_webid(referer_url)
        comment_lsit_req_url = f"https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&cursor=0&count=20&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&update_version_code=170400&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid={webid}&verifyFp=verify_lwg2oa43_Ga6DRjOO_v2cd_4NL7_AHTp_qMKyKlDdoqra&fp=verify_lwg2oa43_Ga6DRjOO_v2cd_4NL7_AHTp_qMKyKlDdoqra&msToken={ms_token}"
        comment_list_headers1 = copy.deepcopy(self.comment_list_headers)
        comment_list_headers1['Referer'] = referer_url
        comment_list_headers1['Cookie'] = f'ttwid={ttwid_str};'
        abogus = self.common_utils.get_abogus(comment_lsit_req_url, self.common_utils.user_agent)
        url = comment_lsit_req_url + "&a_bogus=" + abogus
        response = requests.request("GET", url, headers=comment_list_headers1,verify=False, timeout=3)
        if (response.text):
            req_json = response.json()
            total = req_json.get('total')
            comments = req_json.get('comments')
            if comments:
                for comment_index in range(len(comments)):
                    comment_item = comments[comment_index]
                    print(f"爬取成功：{comment_item.get('user').get('nickname')}：{comment_item.get('text')}")
            else:
                print(f"爬取结束：评论数={total}")
        else:
            print(f"爬取失败或没有评论")

    def get_awery_list(self, req_url,keyword,offet,status):
        if ('modal_id' in req_url):
            aweme_id = parse_qs(urlparse(req_url).query).get('modal_id')[0]
        else:
            aweme_id = urlparse(req_url).path.split("/")[-1]
        referer_url = f"https://www.douyin.com/discover?modal_id={aweme_id}"
        ms_token = self.common_utils.get_ms_token()
        ttwid_str, webid = self.common_utils.get_ttwid_webid(referer_url)
        webid="7365729216689964583"
        # comment_lsit_req_url = f"https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&enable_history=1&keyword={quote(keyword)}&search_source=search_history&query_correct_type=1&is_filter_search=0&from_group_id=&offset={offet}&count=10&need_filter_settings=0&search_id=20240528151351D62EC61004DB86084CB1&update_version_code=170400&pc_client_type=1&version_code=190600&version_name=19.6.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=125.0.0.0&browser_online=true&engine_name=Blink&engine_version=125.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid={webid}&msToken={ms_token}"
        comment_lsit_req_url=f"https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&enable_history=0&keyword={quote(keyword)}&search_source=normal_search&query_correct_type=1&is_filter_search=0&from_group_id=&offset={offet}&count=10&need_filter_settings=0&list_type=single&search_id=202407261559442C0EE22992743904B3E1&update_version_code=170400&pc_client_type=1&version_code=190600&version_name=19.6.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=126.0.0.0&browser_online=true&engine_name=Blink&engine_version=126.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid={webid}&msToken={ms_token}"
        # comment_lsit_req_url = f"https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&cursor=0&count=20&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&update_version_code=170400&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid={webid}&verifyFp=verify_lwg2oa43_Ga6DRjOO_v2cd_4NL7_AHTp_qMKyKlDdoqra&fp=verify_lwg2oa43_Ga6DRjOO_v2cd_4NL7_AHTp_qMKyKlDdoqra&msToken={ms_token}"
        # comment_list_headers1 = copy.deepcopy(self.comment_list_headers)
        comment_list_headers1 = copy.deepcopy(Config.dy_header)
        comment_list_headers1['Referer'] = referer_url
        ttwid_str='1%7CwRY8mMIob7lLIgz8t8zRStldomxFLD_Ijd-MbjLGfkE%7C1721961740%7C7058357965c79622677759f26f811e3680a4cb13addcae91dd11196d88314be1'
        # comment_list_headers1['Cookie'] = f'ttwid={ttwid_str};'
        abogus = self.common_utils.get_abogus(comment_lsit_req_url, self.common_utils.user_agent)
        url = comment_lsit_req_url + "&a_bogus=" + abogus
        proxles = {"http": "http://123.182.58.137:8089", "https": "http://123.182.58.137:8089"}
        proixe = Proxie()
        if status==1:
            response1=proixe.gethsProxie()
        else:
            response1 = proixe.getProxie()
        if response1 is not None:
            proxles['http'] = 'http://' + response1
            proxles['https'] = 'http://' + response1
            response = requests.request("GET", url, headers=comment_list_headers1, verify=False, timeout=3,proxies=proxles)
            print(response.text)
            return response.json()
        return {}


if __name__ == '__main__':
    req_url = "https://www.douyin.com/discover?modal_id=7488208113342958848"
    dy_comment = DyComment()
    dy_comment.get_comment_list("7489475298543570211")