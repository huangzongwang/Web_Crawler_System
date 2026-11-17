import json
import re

import  requests
# from xhs import XhsClient

# from src.sentiment import aliyun_oss_comment
# from src.source.db import DBHelper, DBHelper1
# from src.utils import Config
# from src.utils.Proxie import Proxie

my_headers = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
]
import random


# def get_one_agent():
#     return random.choice(my_headers)
# user_agent=get_one_agent()
# url=f"https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&enable_history=1&keyword=%E8%B5%9B%E4%B9%90%E8%B5%9B&search_source=normal_search&query_correct_type=1&is_filter_search=0&from_group_id=&offset=0&count=10&need_filter_settings=1&list_type=single&update_version_code=170400&pc_client_type=1&version_code=190600&version_name=19.6.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=125.0.0.0&browser_online=true&engine_name=Blink&engine_version=125.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=8.75&effective_type=4g&round_trip_time=50&webid=7365729216689964583&msToken=MvOCloZ78b7EcrhBIoirnhb06_b5DW4GPjDs7nxUN73Q2Uw77WUrH3-ShSDwiiFUNG6_QX0hz7RbSSGMomhWSsMT7RWSFubVmm-fdxuxakiouZAe_3G_tk4w7LLCP9s%3D"
#             #
# def get_ab( url, userAgent, appVersion):
#     p = subprocess.Popen(['node', './a_bogus', url,userAgent,appVersion], stdout=subprocess.PIPE)
#     url = p.stdout.read().strip()
#     return url
#
# print(get_ab(f"{url}",user_agent,user_agent.replace("Mozilla/","")))
# header={
#      "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
#     "accept": "application/json, text/plain, */*",
#     "sec-ch-ua-mobile": "?0",
#     "user-agent":  get_one_agent(),
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-site": "same-origin",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-dest": "empty",
#     "referer": f"https://www.douyin.com/?recommend=1",
#     "Priority": "u=1, i"
# }
# print(header)
# def get_ab(url):
#     p = subprocess.Popen(['node', './a_bogus', url], stdout=subprocess.PIPE)
#     url = p.stdout.read().strip()
#     return url
#
#  url1=f"https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&enable_history=1&keyword=%E8%B5%9B%E4%B9%90%E8%B5%9B&search_source=normal_search&query_correct_type=1&is_filter_search=0&from_group_id=&offset=0&count=10&need_filter_settings=1&list_type=single&update_version_code=170400&pc_client_type=1&version_code=190600&version_name=19.6.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=125.0.0.0&browser_online=true&engine_name=Blink&engine_version=125.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=8.75&effective_type=4g&round_trip_time=50&webid=7365729216689964583&msToken=MvOCloZ78b7EcrhBIoirnhb06_b5DW4GPjDs7nxUN73Q2Uw77WUrH3-ShSDwiiFUNG6_QX0hz7RbSSGMomhWSsMT7RWSFubVmm-fdxuxakiouZAe_3G_tk4w7LLCP9s%3D"
#     #
# print(get_ab(f"{url1}"))
# https://mcs.zijieapi.com/webid
# {"app_id":2018,"url":"https://www.douyin.com/","user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","referer":"https://www.douyin.com/","user_unique_id":""}
# res=requests.post("https://ttwid.bytedance.com/ttwid/union/register/",json={"region":"cn","aid":1768,"needFid":False,"service":"www.ixigua.com","migrate_info":{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":True})
# print(res.request.headers)
# print(res.headers)
# print(res.headers['Set-Cookie'].split(';')[0].replace("ttwid=",""))
# print(res.text)
# headers = {
#                 "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
#                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#                 "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
#             }
# res=requests.post("https://mcs.zijieapi.com/webid",json={"app_id":2018,"url":"https://www.douyin.com/","user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","referer":"https://www.douyin.com/","user_unique_id":""},headers=headers)
# print(res.request.headers)
# print(res.headers)
# print(res.text)
#
# def get_ttwid_webid( req_url):
#     while True:
#         try:
#             headers = {
#                 "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
#                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#                 "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
#             }
#
#             response = requests.request("GET", req_url, headers=headers, verify=False, timeout=3)
#             cookies_dict = response.cookies.get_dict()
#             ttwid_str = cookies_dict.get('ttwid')
#             render_data_text = \
#                 re.compile('\<script id=\"RENDER_DATA\" type\=\"application\/json\">(.*?)\<\/script\>').findall(
#                     response.text)
#             if (render_data_text):
#                 render_data_text = render_data_text[0]
#                 render_data_text = requests.utils.unquote(render_data_text)
#                 render_data_json = json.loads(render_data_text, strict=False)
#                 webid = render_data_json.get('app').get('odin').get('user_unique_id')
#                 return ttwid_str, webid
#         except Exception as e:
#             print(e)
# referer_url = f"https://www.douyin.com/discover?modal_id={7293455479869541686}"
# ttwid_str, webid=get_ttwid_webid(referer_url)
# print(ttwid_str)
# print(webid)

# res=requests.get("https://share.proxy.qg.net/get?key=95EB3A01&num=1&area=&isp=0&format=txt&seq=\r\n&distinct=false")
# print(res.text)
# proxles = {"http": "http://125.77.162.10:20046", "https": "http://125.77.162.10:20046"}
# proxles['http'] = 'http://' + res.text.strip()
# proxles['https'] = 'http://' + res.text.strip()
# print(proxles)
# res=requests.get("https://www.douyin.com",proxies=proxles)
# print(res.text)
#

# # 打开两个文件
# with open('order_recorecord.txt', 'r') as file1, open('185585.txt', 'r') as file2:
#     # 读取文件内容
#     content1 = file1.read()
#     content2 = file2.read()
#
# # 比较文件内容
# data1=content1.split("\n")
# data2=content2.split("\n")
# for data2_in in data2:
#     for data1_in in data1:
#         if data1_in.strip() == data2_in.strip():
#             print("")
#         else:
#             print(data2_in)

# 提前准备好三个txt文件
# 1.txt 和 2.txt 为对比文件
# diff.txt 为存储不同内容文件

# 以读取方式打开两个txt文件
# f1 = open("185585.txt","r")
# f2 = open("order_recorecord.txt","r")
#
# # 读取两个txt文件
# txt1 = f1.read()
# txt2 = f2.read()
# # 按行的方式读取txt文件
# #txt1 = f1.readline()
# #txt2 = f2.readline()
#
# # 释放两个文件进程
# f1.close()
# f2.close()
#
# # 将两个文件中内容按空格分隔开
# line1 = txt1.split()
# line2 = txt2.split()
#
# # 以读取方式打开 diff.txt 文件
# outfile = open("diff.txt", "w")
#
# # 循环遍历1号文件中的元素
# for i in line1:
# 	# 查看1中文件是否在2中存在
# 	if i not in line2:
# 		outfile.write(i+"\n")
# outfile.write("Above content in 1. But not in 2.")
# for j in line2:
# 	# 查看2中文件是否在1中存在
# 	if j not in line1:
# 		outfile.write(j+"\n")
# outfile.write("Above content in 2. But not in 1.")
# print("核对结束")
#
#
# '''
# file1 = "1.txt"
# file2 = "2.txt"
# f_diff = "diff.txt"
# # ---------- 对比文件内容，输出差异
# f1 = open(file1, "r")
# f2 = open(file2, "r")
# file1 = f1.readlines()
# file2 = f2.readlines()
# f1.close()
# f2.close()
# outfile = open(f_diff, "w")
# flag = 0
# outfile.write("file1独有的数据：\n")
# for i in line1:
#     if i not in line2:
#         outfile.write(i)
#         flag = 1
# outfile.write("file2独有的数据：\n")
# for i in line2:
#     if i not in line1:
#         outfile.write(i)
#         flag = 1
# outfile.close()
# if flag == 1:
#     print("数据存在差异，请仔细核对！")
# '''
# headers = {
#                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0  Safari/537.36",
#                 "Accept": "text/html,application/xhtml+xml, application/xml;q=0 .9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0",
#                 "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
#                 "Connection": "keep-alive",
#                 # "Accept-Encoding": "gzip, deflate, br",
#                 # "Host": "www.baidu.com",
#                 # 需要更换Cookie
#                 "Cookie": "",
#             }
# req = requests.get("https://v.douyin.com/i6rEK8DY/", headers=headers, allow_redirects=False)
# print(req.headers.get('Location').split("/?")[0].replace("https://www.iesdouyin.com/share/video/", ""))

# from xhs.help import (cookie_jar_to_cookie_str, download_file,
#                    get_imgs_url_from_note, get_search_id, get_valid_path_name,
#                    get_video_url_from_note, parse_xml, sign,
#                    update_session_cookies_from_cookie)
# signs = sign("https://edith.xiaohongshu.com/api/sns/web/v1/feed", {"source_note_id":"660aaf3200000000040192d4","image_formats":["jpg","webp","avif"],"extra":{"need_body_topic":"1"},"xsec_source":"pc_search","xsec_token":"ABIiBv_O-NaDIEki3jcH9JZ39hIkPETVcee8yC6xJl2YY="}, a1="18f51ab0d735h7bpiopjwbvgcqgilwkxvwfevzhvv50000426295")
# print(signs["x-s"])
# res=requests.post("https://edith.xiaohongshu.com/api/sns/web/v1/feed",headers=headers,json=
# {"source_note_id":"660aaf3200000000040192d4","image_formats":["jpg","webp","avif"],"extra":{"need_body_topic":"1"}})
# print(res.text)
# xhs_client = XhsClient(Config.xhs_Cookie)
# notes = xhs_client.get_note_by_id("663aeff1000000001e023187")
# consumer=notes['video']['consumer']
# url="https://sns-video-bd.xhscdn.com/"+consumer['origin_video_key']
# print(url)
# data = DBHelper.query_db("select * from sentiment_material")
# for i in data:
#     print(i)
#     sql = "INSERT INTO `video_info` (`videoId`, `keyword`, `platform`,`location`,`title`,`status`) VALUES (%s, %s, %s,%s, %s, %s)"
#     values = (i[0], i[1], i[2],  i[3], i[4],i[5])
#     DBHelper1.insert_db(sql,values)
# data = DBHelper1.query_db("select * from sentiment_keyword_status where xhs_status=0 limit 1")

# data = DBHelper1.query_db("select * from video_info where location='' and platform='小红书' limit 1")
# print(data)
# 读取文件内容
# 读取文件内容
# with open('list.txt', 'r') as file:
#     lines = file.readlines()
#
# # 去重
# unique_lines = set(lines)
#
# # 写回文件
# with open('list.txt', 'w') as file:
#     file.writelines(unique_lines)
# oss = aliyun_oss_comment.OssService()
# oss.tqdm_download( "11.mp4", "http://v3-web.douyinvod.com/d3f0e7d3291affbe3ec7e31d772c8199/6690c5cc/video/tos/cn/tos-cn-ve-15c001-alinc2/oEAl04IgD4AfBhKdCyeSBUN6n2zqABQEqQ3y1h/?a=6383\u0026ch=11\u0026cr=3\u0026dr=0\u0026lr=all\u0026cd=0%7C0%7C0%7C3\u0026cv=1\u0026br=659\u0026bt=659\u0026cs=0\u0026ds=4\u0026ft=AJkeU_TERR0s~hC32D12Nc0iPMgzbLK7W8sU_4O_Bw2JNv7TGW\u0026mime_type=video_mp4\u0026qs=0\u0026rc=NDtoaTtpOmYzODs5ZDVlZkBpamxweDQ6ZnZvbDMzNGkzM0AtLi5iMS81X2MxXzZfMy4uYSMtaGhucjQwamRgLS1kLTBzcw%3D%3D\u0026btag=80000e00028000\u0026cquery=100z_100o_101n_100B_100x\u0026dy_q=1720752846\u0026feature_id=f0150a16a324336cda5d6dd0b69ed299\u0026l=20240712105405A2A29169E628BF48179F")
# res=requests.get("",headers=Config.dy_header)
# print(res.headers)
# print(res.text)

import requests

# data = DBHelper1.query_db("select * from video_info where videoId='3xj5n728dzzyaj0'")
# print(data)
# if len(data)>0:
#     print("--------------------")
# else:
#     print("2322434352325")
# req = requests.get("http://xhslink.com/uLNtqP", allow_redirects=False)
# print(req.headers.get('Location'))

# dy_header = {
#      "Host": "www.douyin.com",
#     "Connection": "keep-alive",
#     "sec-ch-ua": "Google Chrome;v=125, Chromium;v=125, Not.A/Brand;v=24",
#     "Accept": "application/json, text/plain, */*",
#     "sec-ch-ua-mobile": "?0",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
#     "sec-ch-ua-platform": "Windows",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Dest": "empty",
#     "Referer": "https://www.douyin.com/video/7364765039644921114",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cookie": "ttwid=1%7CsR3rVSba0OrXdyijyymHeC_1u6vSLwUv5N8NGPpig9k%7C1714967493%7Cfaf2e90ab915026717b74cb09dd113d64d400941e19ae77f2a2ef687e21002a6; bd_ticket_guard_client_web_domain=2; SEARCH_RESULT_LIST_TYPE=%22single%22; UIFID_TEMP=29d6bea3e5a6c157a08a212e1912b5e8a78666ece26be56100fa19e58a63a45b18e84b3c21d3f0f2b0f9ecc0aa58a67b1a248997f136535c26be30cf2ecff98ae546654ac99fe76365c79f7cb3994507; UIFID=29d6bea3e5a6c157a08a212e1912b5e8a78666ece26be56100fa19e58a63a45b6eec83a382132c2e52db5f2690dac763acd13c00f881883c0ee0d84769895280113c48b2ee54218bc6d2b6f820feadbf9e5ade60a74f69134df9ceda19bc10d0aa769c11c7c2ea29ebfbe11fb48b8053d2e8129ce35a13edeb972fea2a54bf4c40117ac3b23185f815705c6d4ed5770d4e9daa72f124e1ead5e71b1987219689; passport_csrf_token=564233cf2141c710636e7baec83c6b44; passport_csrf_token_default=564233cf2141c710636e7baec83c6b44; is_staff_user=false; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; store-region-src=uid; my_rd=2; d_ticket=a053c4387185e76d4ddac3d17427b71c9f7e4; passport_assist_user=CjyrK0Iw7xS37U3wJJHXRji_fJe_hQmlTkSTKNcnwWYzy8rVIMlYZjkLY4GThzB6_sayJkDmiAraTM6NFpQaSgo8A1IA9PQZ5SvATiXe4hMUKP2Bnaah34QETTcqcAj-on-cL4mR0vcSU0PAoj2B-SvPIboz0iEWchgNfx_VELvW1w0Yia_WVCABIgEDaD4vIw%3D%3D; n_mh=eqGn3kR2aKQuug3nOv98c5xP01S4w0EjSO78rjf1mNA; sso_uid_tt=7e4a40eebfaf590a66bc22c9339cfb1b; sso_uid_tt_ss=7e4a40eebfaf590a66bc22c9339cfb1b; toutiao_sso_user=df1e7d7cc86a53b4ff5fcb82e2ad76e4; toutiao_sso_user_ss=df1e7d7cc86a53b4ff5fcb82e2ad76e4; sid_ucp_sso_v1=1.0.0-KDQ2OTQxMDhlMzVjMGFjMWI2OTdlYWIyNWYzMWRhYzk4NDlkOTA2OWEKHwiE5aKzjgIQ2ruNtQYY7zEgDDCP5ZvPBTgCQPEHSAYaAmxmIiBkZjFlN2Q3Y2M4NmE1M2I0ZmY1ZmNiODJlMmFkNzZlNA; ssid_ucp_sso_v1=1.0.0-KDQ2OTQxMDhlMzVjMGFjMWI2OTdlYWIyNWYzMWRhYzk4NDlkOTA2OWEKHwiE5aKzjgIQ2ruNtQYY7zEgDDCP5ZvPBTgCQPEHSAYaAmxmIiBkZjFlN2Q3Y2M4NmE1M2I0ZmY1ZmNiODJlMmFkNzZlNA; uid_tt=5f1caa6c2398c217970eb1c0888d421e; uid_tt_ss=5f1caa6c2398c217970eb1c0888d421e; sid_tt=a0b2a73b437e17bfd7a57a4f22fbeb63; sessionid=a0b2a73b437e17bfd7a57a4f22fbeb63; sessionid_ss=a0b2a73b437e17bfd7a57a4f22fbeb63; _bd_ticket_crypt_cookie=1159b093bada18097eac70c059ec032b; store-region=cn-fj; sid_guard=a0b2a73b437e17bfd7a57a4f22fbeb63%7C1724032196%7C5184000%7CFri%2C+18-Oct-2024+01%3A49%3A56+GMT; sid_ucp_v1=1.0.0-KDY4ODE4ZmIzOGU5MGU4MjAyNDFlNzhkNThlYzIzNWM2ZTM3ZDYzMDcKGQiE5aKzjgIQxMmKtgYY7zEgDDgCQPEHSAQaAmhsIiBhMGIyYTczYjQzN2UxN2JmZDdhNTdhNGYyMmZiZWI2Mw; ssid_ucp_v1=1.0.0-KDY4ODE4ZmIzOGU5MGU4MjAyNDFlNzhkNThlYzIzNWM2ZTM3ZDYzMDcKGQiE5aKzjgIQxMmKtgYY7zEgDDgCQPEHSAQaAmhsIiBhMGIyYTczYjQzN2UxN2JmZDdhNTdhNGYyMmZiZWI2Mw; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.99%7D; hevc_supported=true; SelfTabRedDotControl=%5B%5D; publish_badge_show_info=%220%2C0%2C0%2C1724665998709%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAQYcsLG7jTJVMpmh8J2leUv3IISG7pqgRRt4u5410kMk%2F1725033600000%2F0%2F0%2F1725004534150%22; strategyABtestKey=%221725259084.271%22; biz_trace_id=05e2740f; download_guide=%223%2F20240902%2F1%22; pwa2=%220%7C0%7C3%7C0%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAQYcsLG7jTJVMpmh8J2leUv3IISG7pqgRRt4u5410kMk%2F1725292800000%2F0%2F1725262014138%2F0%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRHl2R013UTNrNGI2NVJ3TjZPK2JCWU93WEpFdnlKajZub1pMeXBPZUtZbE1yOXFpQ0lOSXdSWU9uaHJ3TXVxc1BRQXNVTGNwazRoUlpvMU4vbUxyb1k9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; WallpaperGuide=%7B%22showTime%22%3A1723010509334%2C%22closeTime%22%3A1722568438498%2C%22showCount%22%3A6%2C%22cursor1%22%3A322%2C%22cursor2%22%3A7%2C%22hoverTime%22%3A1721202407527%7D; odin_tt=d1b0e0b39daa762b8646f4d569ea87541f782b4c5099b6de66837257740b08e7fc156e24b345af744cddafa1cb44a9eb; IsDouyinActive=false"

#   }
# url="https://www-hj.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7396633833451310345&update_version_code=170400&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=false&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=124.0.0.0&browser_online=true&engine_name=Blink&engine_version=124.0.0.0&os_name=Windows&os_version=10&cpu_core_num=20&device_memory=8&platform=PC&downlink=7.5&effective_type=4g&round_trip_time=100&webid=7365729216689964583&msToken=BynakogeRNYO-OKIh8Eviq2frkXchVXl-qaAlE-N97Gd0Pv3c8u7Z4H2IhU2PhMqsRf6R0DLkS0antOZas8VbZs1zQtWW4Y7vbNNFzkQVh3y03uaDQrl25kC9Exgjs0%3D&a_bogus=O7RMQd0XDkgBXDSh53ILfY3q66r3YQeW0trEMD2f1V3rWL39HMO%2F9exLsFvvKEbjN4%2FkIeEjy4hbYp%2FgrQAjMZwf7Wsx%2F2CZsg00t-P2so0j53intL6mE0hN5kb3SFlm5XNAEOJ0y75azbz0AoKcmhK4bfebY7Y6i6trjD%3D%3D&verifyFp=verify_lz2fv2ce_9e1727af_3e29_a9d9_0e36_befd5401c7a3&fp=verify_lz2fv2ce_9e1727af_3e29_a9d9_0e36_befd5401c7a3"
# rsp=requests.get(url,headers=dy_header)
# print(rsp.json())

# from blind_watermark import WaterMark

# bwm1 = WaterMark(password_img=1, password_wm=1)
# bwm1.read_img('C:\\Users\\admin\\Desktop\\5f188137979d8796f94cf8a4895d1d3.jpg')
# wm = '@guofei9987 开源万岁！'
# bwm1.read_wm(wm, mode='str')
# bwm1.embed('C:\\Users\\admin\\Desktop\\5f18813.jpg',100)
# len_wm = len(bwm1.wm_bit)
# print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
# bwm1 = WaterMark(password_img=1, password_wm=1)
# wm_extract = bwm1.extract('C:\\Users\\admin\\Desktop\\5f18813.jpg', wm_shape=len_wm, mode='str')
# print(wm_extract)
from datetime import datetime
import requests 
# GET  HTTP/1.1
# Host: f.video.weibocdn.com
# Connection: keep-alive
# Pragma: no-cache
# Cache-Control: no-cache
# sec-ch-ua-platform: "Windows"
# Accept-Encoding: identity;q=1, *;q=0
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
# sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
# sec-ch-ua-mobile: ?0
# Accept: */*
# Sec-Fetch-Site: cross-site
# Sec-Fetch-Mode: no-cors
# Sec-Fetch-Dest: video
# Referer: https://weibo.com/
# Accept-Language: zh-CN,zh;q=0.9
# Range: bytes=0-
# header={
#     "Host": "f.video.weibocdn.com",
#     "Connection": "keep-alive",
#     "Pragma": "no-cache",
#     "Cache-Control": "no-cache",
#     "sec-ch-ua-platform": "Windows",
#     "Accept-Encoding": "identity;q=1, *;q=0",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
#     "sec-ch-ua": "Google Chrome;v=131, Chromium;v=131, Not_A Brand;v=24",
#     "sec-ch-ua-mobile": "?0",
#     "Accept": "*/*",
#     "Sec-Fetch-Site": "cross-site",
#     "Sec-Fetch-Mode": "no-cors",
#     "Sec-Fetch-Dest": "video",
#     "Referer": "https://weibo.com/",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Range": "bytes=0-",
# }

# data=requests.get('https://f.video.weibocdn.com/o0/IzBvv8aQlx08k7Z2xIGY01041200ja9Q0E010.mp4?label=mp4_720p&template=720x1280.24.0&media_id=5108331908366389&tp=8x8A3El:YTkl0eM8&us=0&ori=1&bf=4&ot=v&ps=3lckmu&uid=3ZoTIp&ab=,8012-g2,8013-g0,3601-g39,3601-g36,3601-g39&Expires=1733469602&ssig=92wIKf0Wi4&KID=unistore,video',headers=header)
# print(data.headers)
# print(data.content)
# with open('re.mp4','wb') as f:        # 保存视频
#     f.write(data.content)
# 
# from sentiment import aliyun_oss_comment
# req=requests.get('https://tbzb.taobao.com/live?spm=tbpc.anchor.0.0.366c1d90yt5MvN&liveSource=pc_live.anchor&liveId=516252356378')
# print(req.text)
# https://livecbing.alicdn.com/mediaplatform/d9182f85-1c62-48eb-9042-80589b30a3d5/41.ts


# content=""
# with open('C:\\Users\\admin\\Desktop\\live.txt', 'r') as file:
#     content = file.read()
# content_list=content.split("\n")
# oss = aliyun_oss_comment.OssService()
# for i,data in enumerate(content_list):
#     if not data.startswith("#EXTINF"):
#         print(data)
#         oss.tqdm_download(str(i)+".ts","https://alivod.a.yximgs.com/livedvr/flv2ts/gifshow/"+data)


# https://alivod.a.yximgs.com/livedvr/flv2ts/gifshow/f84vTgETYWE_AuditAvcOriginL4.1733393793021.txhbs2.ts?auth_key=1735260167-1011882525-0-e040626d2d32a64f8db3b858e040698b
# https://alivod.a.yximgs.com/livedvr/flv2ts/gifshow/f84vTgETYWE_AuditAvcOriginL4.1733393793021-2520577.0-16.m3u8?auth_key=1735260167-1011882525-0-e040626d2d32a64f8db3b858e040698b
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(current_time)
res=requests.get("https://wxgocrm.jiangxisls.com/api/v1/ShopOrder/get_jd_deorder_list?start_time=2025-08-25&end_time=2025-08-26&page=1&paginate=5000",headers={'Myhsign': '6135acb60fa6ced41c1b6e7ed7f183e913'})
respon=res.json()
arr = respon["data"]["data"]
print("开始执行，执行数量为："+str(len(arr)))
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(current_time)