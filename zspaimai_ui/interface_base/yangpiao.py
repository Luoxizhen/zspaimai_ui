import requests
def get_bid_history_data(p,nid,rid):
    # url = "https://yangpiao.com/Users/getBidHistoryData?page=5&_t=1655284669029&certPick=&certCo=&dealTimeStr=&specimen=&nId=64&rId=2"
    url = "https://yangpiao.com/Users/getBidHistoryData"
    headers = {

        "cookie":"_ypuuid=5a28b9493c191fdd897d4e2cdc60c5c5",
        "cookie": "Hm_lpvt_6ce79aaf03f417b904b3b0bf01ba5e87=1658195539",
        "cookie":"Hm_lvt_6ce79aaf03f417b904b3b0bf01ba5e87=1658195485",
        "cookie": "__51cke__=",
        "cookie": "__51laig__=3",
        "cookie": "__51vcke__JHpoW8doII8bLRu4=bd27ff17-1718-552c-a0f0-7782ca4bc62b",
        "cookie": "__51vuft__JHpoW8doII8bLRu4=1658195485104",
        "cookie": "__tins__21009109=%7B%22sid%22%3A%201658195533618%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201658197338623%7D",
        "cookie":"__vtins__JHpoW8doII8bLRu4=%7B%22sid%22%3A%20%2269d196b9-c5b7-57a2-9505-3f3651d3b11e%22%2C%20%22vd%22%3A%206%2C%20%22stt%22%3A%2053526%2C%20%22dr%22%3A%20209%2C%20%22expires%22%3A%201658197338628%2C%20%22ct%22%3A%201658195538628%7D",
        "cookie": "mh_0.5782959105404446=12345",
        "cookie": "__51uvsct__JHpoW8doII8bLRu4=1",
        "cookie": "__51cke__=",

        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q = 0.9",
        "access-token": "da0d9dddef43f73735802534513ec423b650588b",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    data={
        "page": p,
        "certPick": "",
        "certCo": "",
        "dealTimeStr": "",
        "specimen": "",
        "nId": nid,
        "rId": rid
    }
    r = requests.request('get', url=url, params=data, headers=headers,verify=False)
    print(r.json())
    return r

if __name__ == "__main__":
    get_bid_history_data(1,2,1)
