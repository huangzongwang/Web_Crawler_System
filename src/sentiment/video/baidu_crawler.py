import requests
from bs4 import BeautifulSoup
import re
import time
import csv
from random import uniform

# 用户代理和Cookie配置（需替换为实际值）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'BAIDUID=8F716A5D9052D2F203ABB81252DC2E3A:FG=1; PSTM=1749536008; BIDUPSID=E067F614782DCAFD9A6C28E369FAEFA4; MAWEBCUID=web_DXdqwwJsbFNPYckIEDRchOJGaucPyiWmpbeYkihBdQJxOcnjFC; MCITY=-138%3A; BDUSS=5Qb0F3dFRZNm1OSllQaUp3UHpzRm5XanRwTXkzdUZaV005OHZ5VTEyZFBHTEZwSVFBQUFBJCQAAAAAAAAAAAEAAACK6BD-Y2Fyc29uMzMyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE-LiWlPi4lpYW; BDUSS_BFESS=5Qb0F3dFRZNm1OSllQaUp3UHpzRm5XanRwTXkzdUZaV005OHZ5VTEyZFBHTEZwSVFBQUFBJCQAAAAAAAAAAAEAAACK6BD-Y2Fyc29uMzMyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE-LiWlPi4lpYW; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS_BFESS=63144_67499_67600_67751_67744_67313_67727_67833_67854_67852_67858_67864_67859_67861_67644_67885_67895_67948_67918_67951_67953_67956_67977_67883_68007_68024_68053_68073_68088_68092; BAIDUID_BFESS=8F716A5D9052D2F203ABB81252DC2E3A:FG=1; H_WISE_SIDS=63144_67499_67600_67751_67744_67313_67833_67854_67852_67858_67864_67859_67861_67885_67895_67948_67918_67951_67953_67956_67977_67883_68007_68024_68053_68073_68088_68092_67985_68002; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BA_HECTOR=0gaga02h24a52004a1242g20250h861kqaldd27; ZFY=WwOW:AXdBcguEGhIRSPmJt724Z24ATx7Q:AlJMuwcNST4:C; BCLID=7236108711180255228; BCLID_BFESS=7236108711180255228; BDSFRCVID=FVCOJexroGWw0h5E6Jtt81DeQRo6HPJTDYrEOwXPsp3LGJLV1B6vEG0PtD6qtMDb6j3fogKK3gOTH4DF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=FVCOJexroGWw0h5E6Jtt81DeQRo6HPJTDYrEOwXPsp3LGJLV1B6vEG0PtD6qtMDb6j3fogKK3gOTH4DF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbC8VCDKJC03H48k-4QEbbQH-UnLqh5e3gOZ04n-ah3RfIJdjf_-y6_heaQRex3Zabc7bpcm3UTKsq76Wh35K5tTQP6rLjoGJjc4KKJxbp--qtbEQ-K-M6tEhUJiB5JMBan7_pbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC0wjj-5D5OBepbyKJ0X5TTh0Rr5aTrjDCk6yJocy4LdjGKJanv73R74_qcLKDPas56ebtbZ3-Kg3-Aq54R7ymQkbM3lthTBsCKCX4K-QfbQhlbOqP-jWaRibU3NQn7JOpkRbUnxy50vQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3Pt6IetRK8oCLaJKvDqTrP-trf5DCShUFsQ4RRB2Q-XPoO3M3bhbPGQjjkW-3bDt8L0UTyJebTafbgy4op8P3y0bb2DUA1y4vpJxDqbeTxoUJ23IQafh6e-6j8DPKebPRiJ-b9Qg-JKpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hIDwejL-jjbM-l-X5to05TIX3b7Efbnq_p7_bJ7KhU-i5N33txLqWH8LVIjgHlbkDIQS0M6xQhFXQtnfXpOe-n7rKhc1QDjIM4QHQT3m5M3BKqOu0PDq2J7hWb3cWKOJ8UbSjMOPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eG-Dq6FDJJIfVbobHJoHjJbGq4bohjPz34b9BtQO-DOx--0M2I5pMlcm55AaQ-Lu0xPqBpOZQgnkQq5vbMnmqPtRXMJkXh5LLGjq0x-jLTnR_tj2BlbDMRFRb4nJyUnybPnnBT3R3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CcJ-J8XMD-lDT5P; H_BDCLCKID_SF_BFESS=tbC8VCDKJC03H48k-4QEbbQH-UnLqh5e3gOZ04n-ah3RfIJdjf_-y6_heaQRex3Zabc7bpcm3UTKsq76Wh35K5tTQP6rLjoGJjc4KKJxbp--qtbEQ-K-M6tEhUJiB5JMBan7_pbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC0wjj-5D5OBepbyKJ0X5TTh0Rr5aTrjDCk6yJocy4LdjGKJanv73R74_qcLKDPas56ebtbZ3-Kg3-Aq54R7ymQkbM3lthTBsCKCX4K-QfbQhlbOqP-jWaRibU3NQn7JOpkRbUnxy50vQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3Pt6IetRK8oCLaJKvDqTrP-trf5DCShUFsQ4RRB2Q-XPoO3M3bhbPGQjjkW-3bDt8L0UTyJebTafbgy4op8P3y0bb2DUA1y4vpJxDqbeTxoUJ23IQafh6e-6j8DPKebPRiJ-b9Qg-JKpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hIDwejL-jjbM-l-X5to05TIX3b7Efbnq_p7_bJ7KhU-i5N33txLqWH8LVIjgHlbkDIQS0M6xQhFXQtnfXpOe-n7rKhc1QDjIM4QHQT3m5M3BKqOu0PDq2J7hWb3cWKOJ8UbSjMOPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eG-Dq6FDJJIfVbobHJoHjJbGq4bohjPz34b9BtQO-DOx--0M2I5pMlcm55AaQ-Lu0xPqBpOZQgnkQq5vbMnmqPtRXMJkXh5LLGjq0x-jLTnR_tj2BlbDMRFRb4nJyUnybPnnBT3R3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CcJ-J8XMD-lDT5P; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGmQOdEN4XCjrKliPOytfDkLGEimjy3MrXEpSuItnI4KD3e2i72NBoDc2aMBcS81g684AGoyO/0Cb8cOEWZvkP2yAtfMKQnc7J4S/+0BaG4hmxJsVwXkGdF24AsEQ3K5XBbh9EHAWDOg2T1ejpq0s2eFz67xpujr1V+of2ZgvZNzVPpaEhZpob9le2b5QIEdiQe/UUOOs2fkuUdvUcIGr3f6FCMUN0p4SXVVUMsKNJv2T2Q0Rs14gDuqHJ3rxHJuOGO4LkPV+7TROLMG0V6r0A++zkWOdjFiy1eD/0R8HcRWYo64YZQejZKa7nFsdjKdPqCp+HBavJhpxl858h16cMtKQmxzisHOxsE/KMoDNYYE7ucLE22Bi0Ojbor7y6SXfVj7+B4iuZO+f7FUDWABtt/WWQqHKVfXMaw5WUmKnfSR5wwQa+N01amx6X+p+x97kkGmoNOSwxWgGvuezNFuiJQdt51yrWaL9Re9fZveXFsIu/gzGjL50VLcWv2NICayyI8BE9m62pdBPySuv4pVqQ9Sl1uTC//wIcO7QL9nm+0N6JgtCkSAWOZCh7Lr0XP6QztjlyD3bkwYJ4FTiNanaDaDYRyoveKVIchqofCK/mPLskqm4p5m8u2VBuLkxMjQnrf94QLEjZ1o422kWKKGcYcISGk66HDxtjKMU4HPNa0dthF7UsHf7NW9eE+gwuTQSa7GLWfOy9+ap4iFBQsmjpefgOF89jAHLbnVUejtrqqvdVSQ/4gzJOb0DGzeEZ5GeyPh2zdJds98a9YgAYMEZ23ka2+gNgREnj1mqZH4HmBtIJWlfRxTg0fATL8GqvWQ4/UDHI1keFBVnYanS4vsc0Vv4r6Ox6qCSA2GVhbcby9TZ0ZP/w8N2tU35oxlseq1LWgPu6XttGgSDD3qzeT+ioGRlVhowqdfR1aHkTtWeGpFIinbqcXU/T4f2hLII9D3g89L//u6BXT+N1h/P8jW6t/XyakANHsTFKyDtdEA/kq0p7AMWXEI9EFQPGJKv0Ijpq/pilxhOcTSFvCMP3YiNJ3REd/6cK75U6uYcAhJpQbMAn8Ml6xFylmJPI5+87sYDAvV3NICTNZdymb5mwlfccpsD2YQGte0wan2iODRDe4PUg==; __bid_n=19b1fdb233480648cfef30; RT="z=1&dm=baidu.com&si=0f849ff1-d061-44ac-aa65-07b74280d49d&ss=mm9xwdk8&sl=1&tt=3y&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=5g"; ab_sr=1.0.1_MTQ1MDcyMDE0MWNhZTk2MjM3MGZhOTNjZmI2YTg2MmU0YmIyOGJhM2Y3YjgwMDM1MmE3ODA0MTQyMTk3NTRhY2RmYjlhYTlhNGQyZDRiOGQ1ZThmNmQ4ODFhNGRjZTE0M2M0NGMzNmRkNTNkOGJiMTk2NmU0ODViN2VhOTllYjE1ZTY0NjUyNGRiMjY4YjRhYjBjMmMyM2U4ZThmM2ExNTQzY2ViMzkxNzVhZmJmZjYxZWQzMGE5YmIwZjhlZTFk; H_PS_PSSID=63144_67499_67600_67751_67744_67313_67833_67864_67859_67861_67885_67895_67948_67918_67951_67953_67956_67977_67883_68007_68024_68053_68073_68088_68092_67985_68002; PSINO=7'  # 通过浏览器开发者工具获取
}

def get_search_page(keyword, page=1):
    """获取百度搜索结果页HTML"""
    try:
        url = "https://www.baidu.com/s"
        params = {
            'wd': keyword,
            'pn': (page-1)*10  # 百度分页参数
        }

        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        print(response.text)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def parse_search_results(html):
    """解析搜索结果"""
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    # 获取普通搜索结果
    for item in soup.find_all('div', class_=re.compile('result( c-container)?')):
        try:
            title = item.find('h3').get_text(strip=True)
            link = item.find('a')['href']
            site = item.find('span', class_='c-color-gray').get_text(strip=True) if item.find('span', class_='c-color-gray') else ""
            results.append((title, link, site))
        except Exception as e:
            continue
    
    return results

def save_to_csv(data, filename='baidu_results.csv'):
    """保存结果到CSV"""
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['标题', '链接', '网站'])
        writer.writerows(data)

def main():
    keyword = input("请输入搜索关键词: ")
    pages = int(input("请输入要爬取的页数(1-10): "))
    
    all_results = []
    for page in range(1, pages+1):
        print(f"正在爬取第{page}页...")
        html = get_search_page(keyword, page)
        if html:
            results = parse_search_results(html)
            all_results.extend(results)
            print(f"获取到{len(results)}条结果")
        time.sleep(uniform(1, 3))  # 随机延迟
    
    if all_results:
        save_to_csv(all_results)
        print(f"共获取{len(all_results)}条结果，已保存到baidu_results.csv")
    else:
        print("未获取到有效结果")

if __name__ == '__main__':
    main()