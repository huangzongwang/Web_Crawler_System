import requests 

class YmiYun:
    header={
        "Host": "api.youshu.youcloud.com",
        "Connection": "keep-alive",
        "Content-Length": "4374",
        "sec-ch-ua": "Not)A;Brand;v=99, Google Chrome;v=127, Chromium;v=127",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-platform": "Windows",
        "x-operation-name": "getLeafletMaterialList",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://console.youshu.youcloud.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://console.youshu.youcloud.com/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "_ga=GA1.1.422051889.1724320743; MEIQIA_TRACK_ID=2l0d5ZN7v4zkA99XclxsUtoCL5j; MEIQIA_VISIT_ID=2l0d5ZG3y8MChqGXeO1uY9BbM0T; localeLanguage=zh; sessionId=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJqdGkiOiIxNzI0MzIwODEwNjZjNzBjMmEzYWNhYyIsImV4cCI6MTcyNDkyNTYxMCwic3ViIjoiMTkzODA4IiwidGVhbV9pZCI6IiIsImF1dGhfdHlwZSI6MX0.0bybbSRGDnweihHOxxTv2thID2Z8z33kZHvrBJamrKhxkiN-nAMXpu-144jFTlG4wImpgwSyvhl_VLZqn2xArg; _ga_QNB91PL4C6=GS1.1.1724320757.1.1.1724320811.0.0.0; tfstk=frJsNjYOzP41TunKcrnFO5P0w3BXHEMrCosvqneaDOBOh-KkWsENQG7jceKW3s3GQKTB-eYwbnJXt-tkmdoG3cXMjtXxz4kPlhxGnF4EUPp_JWIJv5IOW7ZH4PWxz4kedzq5Vtd2-ETTOHQhcGEODEEdJwj_HtQOMyFd2wBAkECA9MIPDZeOD1KKAibdktBxZJZ5cf_MfDn1xlvU3YxGR-e7qM1tRhV4U8JCf19vXws1fps11aCU7RjeBe-vQdfnTWXDYQTXMEcztOtv6OIyjAwCehdehMJq0S_9Sptpp6ZzU1OAc_BAOoevAObfwdX-eysH9hRvIFZbHGvwUs_lOmecg9pPwQL_m0xdBiLcZKuuINKvqLAPFvPOeHOvPIsPm87SeDFbA_2fAaoIASVcmsD0R1cx5Q5OxG1EADa9i1IhAaoIASVc6Mj14DiQWIf..; searchQuery=%5B%22%E5%87%8F%E8%82%A5%22%2C%22%E6%B8%A9%E5%8D%9A%E5%A3%AB%22%5D; _ga_BBSDYQEVYB=GS1.1.1724378554.1.1.1724378557.0.0.0; _ga_SFG2Z62L10=GS1.1.1724395302.4.1.1724395329.0.0.0; videoMuted=false; videoVolume=1; ph_oEY7uwNI-BrLK7aN1Al8D1-abXKFEeENlm9zn5gOvzM_posthog=%7B%22distinct_id%22%3A%22193808%22%2C%22%24sesid%22%3A%5B1724395656428%2C%2201917df8-9396-7d0c-9dd9-d9f30de6a2e8%22%2C1724395328406%5D%7D"
    }
    def getData(self,page):
        req_data={"operationName":"getLeafletMaterialList","query":"\n            query getLeafletMaterialList (\n                $category: String\n                $channel: String\n                $platform: String\n                $keyword: String\n                $city: String\n                $format: String\n                $mtype: String\n                $special: String\n                $isLiveMaterial: Int\n                $page: Int\n                $startDate: LocalDate\n                $endDate: LocalDate\n                $order: MaterialListSort\n                $videoTime: String\n                $resolution: String\n                $isExact: Boolean\n                $productId: [String]\n                $sellerCompanyId: String\n                $shopId: String\n                $uid: NumID\n                $liveId: NumID\n                $site: String\n                $brandId: NumID\n                $linesDigest: MixID\n                $isProductAd: Int\n                $ratios: String\n                $materialTag: String\n                $words: String\n                $tpl: [String]\n                $material_score_gte: Int\n                $material_score_lte: Int\n                $searchField: LeafletSearchField\n                $min_price: NumStr\n                $max_price: NumStr\n                $targetingAudience: String\n            ) {\n                leafletMaterialList(\n                    category: $category\n                    channel: $channel\n                    platform: $platform\n                    keyword: $keyword\n                    city: $city\n                    format: $format\n                    mtype: $mtype\n                    special: $special\n                    isLiveMaterial: $isLiveMaterial\n                    page: $page\n                    startDate: $startDate\n                    endDate: $endDate\n                    order: $order\n                    videoTime: $videoTime\n                    resolution: $resolution\n                    isExact: $isExact\n                    productId: $productId\n                    sellerCompanyId: $sellerCompanyId\n                    shopId: $shopId\n                    uid: $uid\n                    liveId: $liveId\n                    site: $site\n                    brandId: $brandId\n                    linesDigest: $linesDigest\n                    isProductAd: $isProductAd\n                    ratios: $ratios\n                    materialTagIds: $materialTag\n                    words: $words\n                    tpl: $tpl\n                    material_score_gte: $material_score_gte\n                    material_score_lte: $material_score_lte\n                    searchField: $searchField\n                    min_price: $min_price\n                    max_price: $max_price\n                    targetingAudience: $targetingAudience\n                ) {\n                    \n        data {\n            \n                material {\n                    \n    durationDefinite\n    materialScoreDefinite\n    cntAdIdDefinite\n    liveCntDefinite\n    cntProductDefinite\n    cnt_product\n    channel {\n        \n    id\n    name\n    icon\n\n    }\n    id\n    material_type\n    duration\n    material_score\n    firstTime\n    lastTime\n    platform {\n        name\n    }\n    cnt_ad_id\n    live_cnt\n    resource {\n        \n    id\n    url\n    height\n    originalUrl\n    size\n    type\n    width\n    poster\n\n    }\n    slogan\n    isCidMaterial\n    impression_inc_2y\n    impressionInc2yDefinite\n\n                    \n                    \n    bgm {\n        title\n        author_name\n    }\n\n                    \n    materialTagList {\n        id\n        name\n    }\n\n                    \n    lines {\n        content\n        lines_style\n    }\n\n                    isCidMaterial\n                    \n                    \n                    productIds\n                    \n                     audienceTagList\n                }\n                highlight\n            \n        }\n        \n            total\n            limit\n            maxTotal\n            page\n        \n    \n                }\n            }\n        ","variables":{"startDate":"2024-05-26","endDate":"2024-08-23","order":"_score_desc","isExact":False,"keyword":"减肥","page":page,"isWord":False,"searchField":"all"}}
        res=requests.post("https://api.youshu.youcloud.com/graphql",json=req_data,headers=self.header)
        return res.json()
    # \\192.168.0.159\策划部视频共享池\有米云数据采集
    def xmlData(self,req_date):
        if 'data' in req_date:
            data=req_date['data']
            if 'leafletMaterialList' in data:
                leafletMaterialList=data['leafletMaterialList']
                if 'data' in leafletMaterialList:
                    leafletMaterialList_data=leafletMaterialList['data']
                    for item in leafletMaterialList_data:
                        if 'material' in item:
                            material=item['material']
                            if 'slogan' in material:
                                slogan=material['slogan']
                            if 'resource' in material:
                                resource=material['resource']
                                for resource_item in resource:
                                    if 'originalUrl' in resource_item:
                                        originalUrl=resource_item['originalUrl']
                                        id=resource_item['id']
                                        #下载

    def run(self,page):
        try:
            res_data=self.getData(page)
            self.xmlData(res_data)
        except Exception as e:
            print('错误了')