import json
import time
from datetime import datetime
import time
import sys
sys.path.append('../')
import schedule
from xhs import FeedType, XhsClient
import requests
from utils import Config
from sentiment import aliyun_oss_comment
oss = aliyun_oss_comment.OssService()



def getXhsComment(noteid,xsec_token,cursor):
    try:
        xhs_client = XhsClient(Config.xhs_Cookie9)
        respon = xhs_client.get_note_comments(noteid, cursor,xsec_token)
        has_more = respon['has_more']
        if has_more:
            cursor1 = respon['cursor']
        comments = respon['comments']
        array = []
        if len(comments) > 0:
            for comment in comments:
                jj = {}
                jj['nickname'] = comment['user_info']['nickname']
                jj['image'] = comment['user_info']['image']
                jj['content'] = comment['content']
                jj['sub_comment_count']=comment['sub_comment_count']
                jj['like_count']=comment['like_count']
                jj['comment_id']=comment['id']
                piv=""
                if 'pictures' in comment:
                    pictures=comment['pictures']
                    if len(pictures)>0:
                        for intdex, pic in enumerate(pictures):
                            oss.tqdm_download(comment['id'] +"_"+str(intdex)+ ".jpg", pic['url_default'])
                            url_image = oss.pushoss(comment['id'] +"_"+str(intdex)+ ".jpg", comment['id'] +"_"+str(intdex)+ ".jpg")
                            piv=piv+url_image
                            if intdex<len(pictures)-1:
                                piv=piv+","
                jj['pictures']=piv
                array.append(jj)
        print(array)
        url = "https://znqcrm.jiangxisls.com/Report/Wapvote2025/get_comment_list"
        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n"+json.dumps(array)+"\n\r\n-----011000010111000001101001--\r\n\r\n"
        headers = {"content-type": "multipart/form-data; boundary=---011000010111000001101001"}
        print(payload)
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.json())
        time.sleep(10)
        if has_more:
            getXhsComment("6874852c000000001c030496","AB2ZF5XxZMoTmZwM00kkdJj1N6UK8Jf5_QJlg1ASW8qEI=",cursor1)
    except Exception as e:
        print(e)    
getXhsComment("6874852c000000001c030496","AB2ZF5XxZMoTmZwM00kkdJj1N6UK8Jf5_QJlg1ASW8qEI=","")