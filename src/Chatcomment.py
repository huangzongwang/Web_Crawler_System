import  requests
#{"messages":[{"role":"user","content":"根据这个改进的写50条出来"}],"use_search":True,"action":"variant","segment_id":"coed8nkascdg3usf526g"}
header={
   "Host": "kimi.moonshot.cn",
    "Connection": "keep-alive",
    "Content-Length": "151",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": "Google Chrome;v=123, Not:A-Brand;v=8, Chromium;v=123",
    "X-Traffic-Id": "cob0591kqq4ttrmrnt8g",
    "sec-ch-ua-mobile": "?0",
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzE2NzgxNiwiaWF0IjoxNzEzMTY2OTE2LCJqdGkiOiJjb2Vka2gxa3FxNHR0cmk2MGlsZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNvYjA1OTFrcXE0dHRybXJudDhnIiwic3BhY2VfaWQiOiJjb2IwNTkxa3FxNHR0cm1ybnQ3ZyIsImFic3RyYWN0X3VzZXJfaWQiOiJjb2IwNTkxa3FxNHR0cm1ybnQ3MCJ9.jAGFMdCMHC0xon2kBlb7G_9d5Fr-8GaeKC0IRgjedKW-rM2Y1wZ9Z4369wAp4uFfvIArEYmzC4PPDncuezjEcQ",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "R-Timezone": "Asia/Shanghai",
    "sec-ch-ua-platform": "Windows",
    "Accept": "*/*",
    "Origin": "https://kimi.moonshot.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://kimi.moonshot.cn/chat/coed7k9kqq4onma5gvug",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cookie": "Hm_lvt_358cae4815e85d48f7e8ab7f3680a74b=1712718390; _ga=GA1.1.139255280.1712718390; Hm_lpvt_358cae4815e85d48f7e8ab7f3680a74b=1713165549; _ga_YXD8W70SZP=GS1.1.1713165226.4.1.1713165550.0.0.0"
}
res=requests.post("https://kimi.moonshot.cn/api/chat/coed7k9kqq4onma5gvug/completion/stream",json={"messages":[{"role":"user","content":"根据这个改进的写50条出来"}],"use_search":True,"action":"variant","segment_id":"coed8nkascdg3usf526g"})
print(res.text)