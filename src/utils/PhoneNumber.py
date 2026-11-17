import re


def getphone(desstr):
    phone = re.findall('(13\d{9}|14[5|7]\d{8}|15\d{9}|166{\d{8}|17[3|6|7]{\d{8}|18\d{9})', desstr)
    return phone


def is_chinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def getwechat(desstr):
    words = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]").sub("-", desstr).replace(":", "-").replace("：", "-").replace(
        "\n", "-").replace("--", "-").replace("--", "-")
    keywords = re.split("-", words)
    wechat = None
    for keyword in keywords:
        # 微信号长度为6-20
        if 6 < len(keyword) < 20:
            chinese = is_chinese(keyword)
            if not chinese:
                wechat = keyword
    return wechat
