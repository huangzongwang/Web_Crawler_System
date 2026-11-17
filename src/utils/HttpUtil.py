import requests


class HttpUtils:
    base_url = "http://webstt.jiangxisls.com"

    def getSendData(self, array, platform,analysis):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        return dd
    def getSendData1(self, array, platform,analysis,keywork):
        dd = {}
        dd["platform"] = platform
        dd["analysis"] = analysis
        dd["data"] = array
        dd['keyword']=keywork
        return dd    

    def sendPost(self, json, platform, url,analysis):
        return requests.post(self.base_url + url, json=self.getSendData(json, platform,analysis))
    

    def sendPost2(self, json, platform, url,analysis,keywork):
        return requests.post(self.base_url + url, json=self.getSendData1(json, platform,analysis,keywork))
    
    def sendPost1(self, json, url):
        print(self.base_url + url)
        return requests.post(self.base_url + url, json=json)

    def sendGet(self, url):
        print(url)
        return requests.get(self.base_url+url)
