import execjs
import base64
import requests
from fastapi import FastAPI, Request
import uvicorn
from datetime import datetime
import time

import schedule

weibo_headers = {
        "Accept":"application/json, text/plain, */*",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"no-cache",
        "Connection":"keep-alive",
        "Cookie":"store-region=cn-gd; store-region-src=uid; gr_user_id=09324404-490a-4a47-aa5d-8aa9a7a03d8b; grwng_uid=452e820f-2932-42da-a01d-158ebcd919e2; _ga=GA1.2.1768042419.1736130048; _ga_6P27KGH9JF=GS1.2.1736820699.2.0.1736820699.0.0.0; _ga_2M3R5Z77SJ=GS1.1.1736820699.2.0.1736820702.0.0.0; aefa4e5d2593305f_gr_last_sent_cs1=1821473182250307; aefa4e5d2593305f_gr_cs1=1821473182250307; is_staff_user=false; is_hit_partitioned_cookie_canary_ss=true; is_hit_partitioned_cookie_canary_ss=true; is_hit_partitioned_cookie_canary=true; is_hit_partitioned_cookie_canary=true; passport_csrf_token=0100fae56a129ad29bad4148029594dd; passport_csrf_token_default=0100fae56a129ad29bad4148029594dd; __security_mc_61_s_sdk_crypt_sdk=bc356769-427f-9a30; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSGlsNGxZKzZrbzJUaGQ1c3Z5dEFHUFFWUTduRk5pMkNOZGtZa0ZpRmhaNDlOcFgzTFNZak9RWmJvbEt5KzJ4TXRjc2FXVnVpWGI4TzRiSVRZdjFaQ2c9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; bd_ticket_guard_client_web_domain=2; passport_mfa_token=Ci8xa2XeTprBxp0olHuj5UIoRMENhoWRyepr8fpxH%2FuR%2B9GJ0UFXR14CLXdqBMNL0hpKCjwAAAAAAAAAAAAAT7pitven7iLZLzIXY%2Bb%2Bl2ZiRx1XNV1Y4aIxPZmkpRNmandA1AtC9bA1B23mzzjUgrIQke2BDhj2sdFsIAIiAQNwIGtX; d_ticket=49f2492e9dbad216cd658c75ea1efdc42bca3; n_mh=27KiXgMkFoZT-cQbKMmHkYV6LeZ8A9e-mlp0zGLxx6U; sso_uid_tt=81e358f3e098ef83c8c076fc69b29e12; sso_uid_tt_ss=81e358f3e098ef83c8c076fc69b29e12; toutiao_sso_user=9d07632f9cc23999ee288ce36f9a5316; toutiao_sso_user_ss=9d07632f9cc23999ee288ce36f9a5316; sid_ucp_sso_v1=1.0.0-KGEwY2Q3NDBhYTYxNDU2NWNkMTM1YWQ2NWIxNjcwYTI2ZjYxYTlkMmIKHwi2_qjciwIQr67wyAYY-gogDDCd-vfOBTgBQOsHSAYaAmxxIiA5ZDA3NjMyZjljYzIzOTk5ZWUyODhjZTM2ZjlhNTMxNg; ssid_ucp_sso_v1=1.0.0-KGEwY2Q3NDBhYTYxNDU2NWNkMTM1YWQ2NWIxNjcwYTI2ZjYxYTlkMmIKHwi2_qjciwIQr67wyAYY-gogDDCd-vfOBTgBQOsHSAYaAmxxIiA5ZDA3NjMyZjljYzIzOTk5ZWUyODhjZTM2ZjlhNTMxNg; __security_mc_61_s_sdk_sign_data_key_sso=db63d4f8-49b5-a48c; __security_mc_61_s_sdk_cert_key=557015db-4929-9332; odin_tt=b9d99a66ca54dc4cd7ed125f13de806608581b419950ddecc5175a37cac6e68e838472012fb3e220e0bf2fadc50052b5; sid_guard=26d79036378dd507970c55305f839b60%7C1763448623%7C5184002%7CSat%2C+17-Jan-2026+06%3A50%3A25+GMT; uid_tt=bae7c3ca0704fe6d7b58dff3aa265cf9; uid_tt_ss=bae7c3ca0704fe6d7b58dff3aa265cf9; uid_tt_ss=bae7c3ca0704fe6d7b58dff3aa265cf9; sid_tt=26d79036378dd507970c55305f839b60; sessionid=26d79036378dd507970c55305f839b60; sessionid_ss=26d79036378dd507970c55305f839b60; sessionid_ss=26d79036378dd507970c55305f839b60; session_tlb_tag=sttt%7C13%7CJteQNjeN1QeXDFUwX4ObYP_________II2PBNYoph8w96omZh8kCTVVvvotYns-lJkr5cZceI_0%3D; session_tlb_tag=sttt%7C13%7CJteQNjeN1QeXDFUwX4ObYP_________II2PBNYoph8w96omZh8kCTVVvvotYns-lJkr5cZceI_0%3D; session_tlb_tag_bk=sttt%7C13%7CJteQNjeN1QeXDFUwX4ObYP_________II2PBNYoph8w96omZh8kCTVVvvotYns-lJkr5cZceI_0%3D; session_tlb_tag_bk=sttt%7C13%7CJteQNjeN1QeXDFUwX4ObYP_________II2PBNYoph8w96omZh8kCTVVvvotYns-lJkr5cZceI_0%3D; sid_ucp_v1=1.0.0-KDViNjVlNDUzZDY5YTMyNjEyNWJlYzQ4N2RkNTQ0MGFjMzliN2U4MjIKGQi2_qjciwIQr67wyAYY-gogDDgBQOsHSAQaAmxxIiAyNmQ3OTAzNjM3OGRkNTA3OTcwYzU1MzA1ZjgzOWI2MA; sid_ucp_v1=1.0.0-KDViNjVlNDUzZDY5YTMyNjEyNWJlYzQ4N2RkNTQ0MGFjMzliN2U4MjIKGQi2_qjciwIQr67wyAYY-gogDDgBQOsHSAQaAmxxIiAyNmQ3OTAzNjM3OGRkNTA3OTcwYzU1MzA1ZjgzOWI2MA; ssid_ucp_v1=1.0.0-KDViNjVlNDUzZDY5YTMyNjEyNWJlYzQ4N2RkNTQ0MGFjMzliN2U4MjIKGQi2_qjciwIQr67wyAYY-gogDDgBQOsHSAQaAmxxIiAyNmQ3OTAzNjM3OGRkNTA3OTcwYzU1MzA1ZjgzOWI2MA; ssid_ucp_v1=1.0.0-KDViNjVlNDUzZDY5YTMyNjEyNWJlYzQ4N2RkNTQ0MGFjMzliN2U4MjIKGQi2_qjciwIQr67wyAYY-gogDDgBQOsHSAQaAmxxIiAyNmQ3OTAzNjM3OGRkNTA3OTcwYzU1MzA1ZjgzOWI2MA; gfkadpd=512179,24451; s_v_web_id=verify_mih3r297_vokhdh4p_wIYf_4fVG_8ECP_eBerIC4JHXZG; ttwid=1%7CfCGCZtTewBWqv-yT2jm5KzcBzc49I1IrzGEc_KpsmzY%7C1764227918%7Cb3ff2895e6ba083e7cf39a5712a69af18c70dba47c72f13bc3a3677b99e603ee; csrftoken=XqfQ-hdUlrozmpH0z6f3S4Zy; gd_random=eyJtYXRjaCI6dHJ1ZSwicGVyY2VudCI6MC4zOTg4MzQzNDY1NjQ0MzE5NX0=.zbSmWsA7+h5iv7URQxJC6keXFxDKY4eu1B85fj9mssw=",
        "Host":"aic.oceanengine.com",
        "Pragma":"no-cache",
        "Referer":"https://aic.oceanengine.com/inspiration/v2?bpId=1698550101023756&id=1637524121608498030",
        "Sec-Ch-Ua":"Not/A)Brand;v=8, Chromium;v=126, Google Chrome;v=126",
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":"Windows",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
def geturl(url):
        weibo_headers['Referer']="https://aic.oceanengine.com/inspiration/v2?"+url
        rep=requests.get("https://aic.oceanengine.com/api/inspiration/get_insight?"+url,headers=weibo_headers)
        print(rep.json())
        if rep.json()['msg']=="ok":
            vid=rep.json()['data']['inspiration']['videos'][0]['videoInfo']['vid']
            print(vid)
            xbogus = execjs.compile(open('./test.js').read()).call('crc32',
                                                                                                vid)
            print(xbogus)
            red=requests.get(xbogus)
            print(red.text)
            try:
                url=base64.b64decode(red.json()['data']['video_list']['video_2']['main_url']).decode('utf-8')
                print(url)
            except :
                url=base64.b64decode(red.json()['data']['video_list']['video_1']['main_url']).decode('utf-8')
                print(url)
                print("-------------")
        else:
            url=rep.json()['msg']     
        return url
# app = FastAPI()

# @app.get('/geturl/bpId={bpId}/id={id}')
# def calculate(bpId, id):
#     url=geturl("bpId="+bpId+"&id="+id)
#     res = {"res":url}
#     return res


# # 主函数入口
# if __name__ == '__main__':
#     # 加载预训练的分词器和模型
#     # 启动FastAPI应用
#     # 用6006端口可以将autodl的端口映射到本地，从而在本地使用api
#     uvicorn.run(app, host='0.0.0.0', port=6009, workers=1)  # 在指定端口和主机上启动应用
#     # getlist("1")
print(geturl("bpId=71865876278&id=1783880685646923"))